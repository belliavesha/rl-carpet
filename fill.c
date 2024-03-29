
#include <stdlib.h>
#include <stdio.h>

void fill(int GD, int genome[GD], int VD, int HD, int field[VD][HD]){
    int prev[VD];
    for (int i=0; i < VD; i++){
        field[i][0]=i;
        prev[i]=0;
    }
    for (int i=0; i < HD; i++){
        field[VD-1][i]=0;
    }
    int g,v,k;
    for (int j=0; j<HD; j++ )
        for (int i = 1; i<VD; i++){
            if (field[i][j]==0) {
                for(k = prev[i-1]+1; k<HD ; k++ ){
                    field[i-1][k]=0;
                }   
                prev[i-1] = HD;
            }else{
                g = genome[field[i][j]];
                v =field[i-1][prev[i-1]];
                if (prev[i-1]+g>=HD) {
                    for(k = prev[i-1]+1; k<HD ; k++ ){
                        field[i-1][k]=v;
                    }   
                    prev[i-1] = HD;
                }else{
                    for(k = 1; k<g ; k++ ){
                        field[i-1][prev[i-1]+k]=v;
                    }
                    prev[i-1] += g;
                    k=v;
                    do k++; while (genome[k]==genome[v]);
                    field[i-1][prev[i-1]]=k;
                }
            }
        }
    return;
        
}

