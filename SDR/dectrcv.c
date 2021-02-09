#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <netinet/ether.h>
#include <linux/if_packet.h>
#include <fcntl.h>
#include <stdlib.h>
#include <inttypes.h>
#include <time.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <poll.h>
#include <assert.h>

static const char clrscr[] = "\33[3;J\33[H\33[2J";

typedef uint64_t time64_t;

#define FP_SYNC		0xAAE98A
#define PP_SYNC		0x551675

static void  hexdump(const uint8_t *d, size_t n) {
	for(;n;n--,d++)
		printf("%02x ",*d);
	//printf("\n");
}

#define GP 0x0589;

static uint16_t calc_rcrc(uint8_t* data)
{
	uint16_t crc;
	uint8_t next;
	int y, x;

	crc=data[0]<<8|data[1];
	y=0;
	while(y<6)	{
		next=data[2+y];
		y++;
		x=0;
		while(x<8)		{
			while(!(crc&0x8000))			{
				crc<<=1;
				crc|=!!(next&0x80);
				next<<=1;
				x++;
				if(x>7)
					break;
			}
			if(x>7)
				break;
			crc<<=1;
			crc|=!!(next&0x80);
			next<<=1;
			x++;
			crc^=GP;
		}
	}
	crc^=1;
	return crc;
}

/* TODOs:
 * GRC: multiple channels, channel setting via xmlrpc */

static int dummy0_open(void) {
	struct sockaddr_ll sa;
	struct ifreq if_idx;
	int sockfd, res;
	
	if ((sockfd = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)) == -1) {
		perror("socket");
	}

	memset(&if_idx, 0, sizeof(struct ifreq));
	strncpy(if_idx.ifr_name, "dummy0", IFNAMSIZ-1);
	if (ioctl(sockfd, SIOCGIFINDEX, &if_idx) < 0)
		perror("SIOCGIFINDEX");
	
	memset(&sa, 0, sizeof(sa));
	sa.sll_ifindex = if_idx.ifr_ifindex;
	sa.sll_halen = ETH_ALEN;
	sa.sll_family = AF_PACKET;
	
	res = bind(sockfd , (struct sockaddr*)&sa, sizeof(sa) );
    assert(!res);
    
    return sockfd;
}

static int fd_nonblock(int sfd) {
        int res, flags = fcntl(sfd,F_GETFL,0);
        assert(flags != -1);
        res = fcntl(sfd, F_SETFL, flags | O_NONBLOCK);
        assert(!res);
        return res;
}

typedef struct __attribute__((packed)) dect_rxhdr_s {
	uint8_t trxmode;
	uint8_t channel;
	uint16_t slot;
	uint8_t frameno;
	uint8_t rssi;
	uint8_t preamble[3];
	uint16_t sync;
} dect_rxhdr_t;

typedef struct __attribute__((packed)) dect_afield_s {
	uint8_t header;
	uint8_t tail[5];
	uint16_t crc;
} dect_afield_t;

enum {
	FP_PKTS,
	PP_PKTS,
	RCRC_ERRORS,
	B_FIELDS,
	
	N_STATS
};

static const char stats_names[N_STATS][16] = {"FP", "PP", "R-CRC errors", "B-fields"};

static time64_t gettime(void) {
	time64_t res;
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	res = ts.tv_sec;
	res *= 1000000000;
	res += ts.tv_nsec;
	return res;
}

typedef struct dectrx_s {
	int sock;
	uint8_t channel;
	uint8_t ethbuf[1024];
	uint64_t sync;
	int bitcnt;
	int frame_len;
	int verbose;
	
	/* stats */
	uint64_t stats[N_STATS];
} dectrx_t;

static void dectrx_stats(dectrx_t *drx, time64_t delta_t, int multi_ch) {
	int i;

	if(multi_ch)
		printf("ch%d: ",drx->channel);
	else
		printf("\r");
	
	for(i=0;i<N_STATS;i++) {
		uint64_t val = drx->stats[i];
		drx->stats[i]=0;
		val *= 1000000000;
		val /= delta_t;
		printf("%s: %5"PRIu64" | ",stats_names[i],val);
	}
	
	if(multi_ch)
		puts("");
	else
		fflush(stdout);
}

static dectrx_t *dectrx_create(uint16_t rxport) {
	struct sockaddr_in si;
	dectrx_t *drx = NULL;
	int sock, res;

	sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	assert(sock >= 0);
	
	memset((char *) &si, 0, sizeof(si));
    si.sin_family = AF_INET;
    si.sin_port = htons(rxport);
    si.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    res = bind(sock , (struct sockaddr*)&si, sizeof(si) );
    assert(!res);
	
	fd_nonblock(sock);
	
	drx = calloc(1, sizeof(dectrx_t));
	
	drx->sock = sock;
	drx->channel = 0xff;
	drx->bitcnt = -1;
	drx->ethbuf[12] = drx->ethbuf[13] = 0x23;
	
	return drx;
}

static int dectrx_rx(dectrx_t *drx, int eth_sock) {
	uint8_t buf[2048], *p=buf, *op;
	int res = recv(drx->sock, buf, sizeof(buf), 0);
	
	if(res <= 0)
		return res;
	
	for(;res;res--,p++) {
		uint32_t syncm;
		int match, i;
		
		for(i=7;i>=0;i--) {
			uint8_t bit = (*p>>i)&1;
			/* find sync */
			drx->sync<<=1;
			drx->sync|=bit;
			syncm = drx->sync & 0xffffff;
			match = (syncm == FP_SYNC) || (syncm == PP_SYNC);
			if(match) {
				uint8_t *op = drx->ethbuf + ETH_HLEN;
				dect_rxhdr_t *rxhdr = (dect_rxhdr_t *)op;
				//printf("%08x\n",syncm);
				rxhdr->channel = drx->channel;
				rxhdr->preamble[2] = (drx->sync>>24)&0xff;
				rxhdr->preamble[1] = (drx->sync>>32)&0xff;
				rxhdr->preamble[0] = (drx->sync>>40)&0xff;
				rxhdr->sync = htons(drx->sync&0xffff);
				drx->bitcnt = 0; /* start frame reception */
				drx->frame_len = sizeof(dect_afield_t);
				drx->stats[(syncm == FP_SYNC) ? FP_PKTS : PP_PKTS]++;
			}
			if(match || (drx->bitcnt < 0))
				continue;

			//printf("%d %d\n",drx->bitcnt>>3,drx->frame_len);
			assert(drx->frame_len >= sizeof(dect_afield_t));
			assert((drx->bitcnt>>3)<=(sizeof(dect_afield_t)+100));
			/* frame reception in progress */
			op = drx->ethbuf + ETH_HLEN + sizeof(dect_rxhdr_t) + (drx->bitcnt>>3);
			*op<<=1;
			*op|=bit;
			drx->bitcnt++;

			/* A-field complete - verify CRC and check if B-field present */
			if(drx->bitcnt == (sizeof(dect_afield_t)<<3)) {
				uint16_t crc = calc_rcrc(drx->ethbuf + ETH_HLEN + sizeof(dect_rxhdr_t));
				dect_afield_t *af = (dect_afield_t *) (drx->ethbuf + ETH_HLEN + sizeof(dect_rxhdr_t));
				uint8_t ba = (af->header>>1)&7;
				int blen;
				
				//puts("AF");
				if(crc) {
					//puts("R-CRC error");
					drx->bitcnt = -1;
					drx->stats[RCRC_ERRORS]++;
					continue;
				}
				
				switch(ba) {
					case 7: 	blen = 0;	break;		/* no B-field */
					case 4:		blen = 10;	break;		/* half slot */
					case 2:		blen = 100;	break;		/* double slot */
					default:	blen = 40;	/* full slot */
				}
				blen += blen ? 1 : 0; /* account for X/Z-fields */
				//printf("%d %d\n",ba, blen);
				drx->frame_len += blen;
				if(blen)
					drx->stats[B_FIELDS]++;
			}
			
			if((drx->bitcnt>>3) == drx->frame_len) {
				/* B-field complete */
				drx->bitcnt=-1;
				send(eth_sock, drx->ethbuf, ETH_HLEN + sizeof(dect_rxhdr_t) + drx->frame_len, 0);
				if(drx->verbose) {
					hexdump(drx->ethbuf + ETH_HLEN + sizeof(dect_rxhdr_t) - 5, drx->frame_len + 5);
					puts("");
				}
			}
		} /* foreach incoming bit */
	} /* foreach incoming byte */
	return 0;
}

int main(int argc, char **argv) {
	int res, eth_sock = dummy0_open();
	int i, channels = 1;
	dectrx_t *drx[10];
	struct pollfd pfds[10];
	time64_t stats_ts;
	
	assert((channels <= 10) && (channels >= 1));
	
	for(i=0;i<channels;i++) {
		drx[i] = dectrx_create(2323+i);
		drx[i]->channel = i;
		pfds[i].fd = drx[i]->sock;
		pfds[i].events = POLLIN;
	}
	
	stats_ts = gettime();
	
	while((res=poll(pfds, channels, 100))>=0) {
		time64_t now = gettime();
		time64_t delta_t = now - stats_ts;
		int stats_update = (delta_t >= 500000000);
		
		if(stats_update) {
			stats_ts = now;
			if(channels > 1)
				puts(clrscr);
		}
		
		for(i=0;i<channels;i++) {
			if(pfds[i].revents)
				dectrx_rx(drx[i], eth_sock);
			if(stats_update)
				dectrx_stats(drx[i], delta_t, (channels > 1));
		}
	} /* poll loop */
	
	return 0;
}
