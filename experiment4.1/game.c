#define _POSIX_C_SOURCE 200809L
#include <sys/socket.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <poll.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
/* Fixed-size, network-byte-order frames: round, moveA, moveB, result. */
static void die(const char*s){perror(s);exit(1);}
static long long now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec*1000LL+t.tv_nsec/1000000;}
static int transfer(int fd,uint32_t*v,int sending,long long end){
 size_t n=0;unsigned char*b=(unsigned char*)v;
 while(n<16){int left=(int)(end-now());if(left<=0)return -1;
 struct pollfd p={fd,sending?POLLOUT:POLLIN,0};
 int r=poll(&p,1,left);if(r<0&&errno==EINTR)continue;if(r<=0)return -1;
 ssize_t k=sending?send(fd,b+n,16-n,MSG_DONTWAIT|MSG_NOSIGNAL):recv(fd,b+n,16-n,MSG_DONTWAIT);
 if(k<0&&(errno==EINTR||errno==EAGAIN))continue;if(k<=0)return -1;n+=(size_t)k;
 }return 0;
}
static int put(int f,int r,int a,int b,int z,long long e){uint32_t v[4]={htonl(r),htonl(a),htonl(b),htonl(z)};return transfer(f,v,1,e);}
static int get(int f,int*v,long long e){uint32_t w[4];if(transfer(f,w,0,e))return -1;for(int i=0;i<4;i++)v[i]=(int32_t)ntohl(w[i]);return 0;}
static void player(int f){
 unsigned seed=(unsigned)time(NULL)^(unsigned)getpid();int v[4];
 while(!get(f,v,now()+60000)&&v[0]>0){int r=v[0];int m=(int)(rand_r(&seed)%3);
 if(put(f,r,m,0,0,now()+2000)||get(f,v,now()+60000))break;
 printf("player %ld round %d: A=%d B=%d result=%d\n",(long)getpid(),r,v[1],v[2],v[3]);
 }close(f);
}
static void judge(int*f,int rounds){
 FILE*out=fopen("result.csv","w");if(!out)die("fopen");
 fprintf(out,"round,A,B,result\n");int count[4]={0};
 for(int r=1;r<=rounds;r++){
 int moves[2]={-1,-1},alive[2]={1,1};long long end=now()+2000;
 for(int i=0;i<2;i++)if(put(f[i],r,0,0,0,end))alive[i]=0;
 for(int i=0;i<2;i++){int v[4];if(alive[i]&&!get(f[i],v,end)&&v[0]==r&&v[1]>=0&&v[1]<3)moves[i]=v[1];}
 int a=moves[0],b=moves[1];
 /* 0 rock, 1 scissors, 2 paper; result 0 draw,1 A,2 B,3 both invalid */
 int z=a<0?(b<0?3:2):(b<0?1:(a==b?0:((a+1)%3==b?1:2)));
 count[z]++;printf("%d,%d,%d,%d\n",r,a,b,z);fprintf(out,"%d,%d,%d,%d\n",r,a,b,z);
 for(int i=0;i<2;i++)put(f[i],r,a,b,z,now()+2000);
 if(a<0||b<0){puts("timeout/invalid/disconnect: match stopped");break;}
 }
 printf("draw=%d A=%d B=%d both_invalid=%d\n",count[0],count[1],count[2],count[3]);
 printf("overall=%s\n",count[1]==count[2]?"draw":count[1]>count[2]?"A":"B");
 for(int i=0;i<2;i++){put(f[i],0,0,0,0,now()+100);close(f[i]);}fclose(out);
}
int main(int argc,char**argv){
 if(argc<2){fprintf(stderr,"local N | server N PORT | client IPv4 PORT\n");return 1;}
 if(!strcmp(argv[1],"client")&&argc==4){int f=socket(AF_INET,SOCK_STREAM,0);if(f<0)die("socket");struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons(atoi(argv[3]));if(inet_pton(AF_INET,argv[2],&a.sin_addr)!=1)return 1;if(connect(f,(void*)&a,sizeof a))die("connect");player(f);return 0;}
 int n=argc>2?atoi(argv[2]):0;if(n<1||n>10000)return 1;int f[2];pid_t p[2];
 if(!strcmp(argv[1],"local")){
 int s[2][2];for(int i=0;i<2;i++)if(socketpair(AF_UNIX,SOCK_STREAM,0,s[i]))die("socketpair");
 for(int i=0;i<2;i++){p[i]=fork();if(p[i]<0)die("fork");if(!p[i]){for(int j=0;j<2;j++){close(s[j][0]);if(j!=i)close(s[j][1]);}player(s[i][1]);exit(0);}f[i]=s[i][0];}
 for(int i=0;i<2;i++)close(s[i][1]);judge(f,n);for(int i=0;i<2;i++)waitpid(p[i],NULL,0);
 }else if(!strcmp(argv[1],"server")&&argc==4){
 int s=socket(AF_INET,SOCK_STREAM,0);if(s<0)die("socket");int yes=1;setsockopt(s,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof yes);
 struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_addr.s_addr=htonl(INADDR_ANY);a.sin_port=htons(atoi(argv[3]));if(bind(s,(void*)&a,sizeof a)||listen(s,2))die("bind/listen");
 puts("waiting for two players");for(int i=0;i<2;i++){f[i]=accept(s,NULL,NULL);if(f[i]<0)die("accept");}close(s);judge(f,n);
 }else return 1;return 0;
}
