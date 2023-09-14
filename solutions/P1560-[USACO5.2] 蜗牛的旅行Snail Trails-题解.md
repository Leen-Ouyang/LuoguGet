
明显这是一道搜索题，其他题解写的有点复杂，我有更简便的写法

既然题目说走到不能再走，那我们就干脆一点，一条路走到黑，不到南墙不回头，一下把要走的路都走完，不但效率高，也好写，关键是大大节省了系统栈

一口气走很多点的关键在于如何记录一个点是否便利过呢？退出后又如何删除标记呢？

或许正是这两个问题使一些想到这种解法的人退缩了，但解决这种问题并不难。我们照常可以用一个二维数组记录一个点是否走过，再用一个栈来记录走过的点，退出时，将栈顶依次弹出就好

也许有人会说don't talk,show me your code.

当然是带着代码来的了，口胡可不是我的风格

```cpp
#include<algorithm>
#include<iostream>
#include<cstring>
#include<cstdio>
#include<cctype>
#define ll long long
#define gc getchar
#define maxn 125
#define maxm 15000
using namespace std;

inline ll read(){
	ll a=0;int f=0;char p=gc();
	while(!isdigit(p)){f|=p=='-';p=gc();}
	while(isdigit(p)){a=(a<<3)+(a<<1)+(p^48);p=gc();}
	return f?-a:a;
}

struct ahaha{
	int x,y;
}s[maxm];   \/\/用一个栈来记录已便利的点的坐标  此处建议使用手写栈，而不是STL的栈
int n,m,ans,a[maxn][maxn];    \/\/ans记录最多能走多少点，a数组表示当前点的状态，1为障碍或边界，0为未访问的点，1是已访问的点
const int xx[4]={1,0,-1,0},yy[4]={0,1,0,-1};
void dfs(int x,int y,int sum){    \/\/x,y表示拐点坐标，sum表示走到当前点已走过的点数（包括当前点）
	int s1=sum;  \/\/s1记录栈大小
	for(int i=0;i<4;++i){
		int xy=x+xx[i],yx=y+yy[i];
		while(!a[xy][yx]){  \/\/若节点可访问，则不断访问直到不能访问
			s[++s1]=(ahaha){xy,yx};a[xy][yx]=2;
			xy+=xx[i],yx+=yy[i];
		}xy-=xx[i],yx-=yy[i];  \/\/最后一个节点不可访问要往回走一个
		if(xy==x&&yx==y)continue;   \/\/如果在原地没动要返回，避免死循环
		ans=max(ans,s1);  \/\/ans利用栈大小赋值
		if(a[xy+xx[i]][yx+yy[i]]!=2)dfs(xy,yx,s1);   \/\/如果下一个点不是已访问的点则继续前进
		while(s1>sum){    \/\/撤销标记，弹出栈顶
			a[s[s1].x][s[s1].y]=0;
			--s1;
		}
	}
}

char c[5];
int main(){
	n=read();m=read();
	while(m--){
		scanf("%s",c+1);int l=strlen(c+1),sum=0;
		for(int i=2;i<=l;++i)
			sum=(sum<<3)+(sum<<1)+(c[i]-48);
		a[c[1]-'A'+1][sum]=1;
	}
	for(int i=1;i<=n;++i)
		a[0][i]=a[n+1][i]=a[i][0]=a[i][n+1]=1;
	a[1][1]=2;s[1]=(ahaha){1,1};   \/\/记得把(1,1)放入栈中，如果不放，答案记得+1
	dfs(1,1,1);    \/\/(1,1)如果不放就是dfs(1,1,0)
	printf("%d\n",ans);
	return 0;
}
```

怎么样是不是简洁又美观呢？喜欢的话，点个赞吧

谢谢您的观看