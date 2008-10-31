/* To compile, run the following command from the root of the iegen source tree: */
/* g++ test.c -g src/dev/ExplicitRelation.c src/dev/RectDomain.c src/dev/util.c src/dev/IAG_cpack.c -o test -I./src/dev */
#include "ExplicitRelation.h"
#include "IAG.h"
#include "util.h"

#define max(a,b) (((a)>(b))?(a):(b))
#define min(a,b) (((a)<(b))?(a):(b))

void inspector(double *fx,double *x,int *inter1,int *inter2,int n_inter,int N,ExplicitRelation **delta,ExplicitRelation **sigma)
{
  /* Declare the index array wrappers */
  ExplicitRelation *inter1_ER,*inter2_ER;

  /* Create the index array wrappers */
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);

  /* Declare sigma_ER */
  ExplicitRelation *sigma_ER=*sigma;

  /* RectDomain for set {[k]: -1k+N+-1>=0 and k>=0 | N} */
  RectDomain *in_domain_A_I_sub_to_x=RD_ctor(1);
  RD_set_lb(in_domain_A_I_sub_to_x,0,0);
  RD_set_ub(in_domain_A_I_sub_to_x,0,N+-1);

  /* Creation of ExplicitRelation of the ARTT */
  /* {[ii]->[k]: k+-1inter1(ii)=0} union {[ii]->[k]: k+-1inter2(ii)=0} */
  ExplicitRelation* A_I_sub_to_x = ER_ctor(1,1,in_domain_A_I_sub_to_x,false);

  /* Define loop body statements */
  #define S1 ER_in_ordered_insert(A_I_sub_to_x,Tuple_make(ii),Tuple_make(ER_out_given_in(inter1_ER,ii)));
  #define S2 ER_in_ordered_insert(A_I_sub_to_x,Tuple_make(ii),Tuple_make(ER_out_given_in(inter2_ER,ii)));

  int ii;
  for (ii=0;ii<=n_inter-1;ii++) {
    S1 ;
    S2 ;
  }

  /* Undefine loop body statements */
  #undef S1
  #undef S2

  /* RectDomain for set {[k]: -1k+N+-1>=0 and k>=0 | N} */
  RectDomain *in_domain_sigma_ER=RD_ctor(1);
  RD_set_lb(in_domain_sigma_ER,0,0);
  RD_set_ub(in_domain_sigma_ER,0,N+-1);

  /* Create sigma */
  *sigma=ER_ctor(1,1,in_domain_sigma_ER,true);
  sigma_ER=*sigma;
  IAG_cpack(A_I_sub_to_x,sigma_ER);

  /* Reorder the data arrays */
  reorderArray((unsigned char*)x,sizeof(double),N+-1-0,sigma_ER);
  reorderArray((unsigned char*)fx,sizeof(double),N+-1-0,sigma_ER);

  /* Destroy the index array wrappers */
  ER_dtor(&inter1_ER);
  ER_dtor(&inter2_ER);
}
void executor(double *fx,double *x,int *inter1,int *inter2,int n_inter,int N,ExplicitRelation **delta,ExplicitRelation **sigma)
{
  /* Declare the index array wrappers */
  ExplicitRelation *inter1_ER,*inter2_ER;

  /* Create the index array wrappers */
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);

  /* Declare sigma_ER */
  ExplicitRelation *sigma_ER=*sigma;

  /* Define the executor main loop body statments */
  /* fx[%(a1)s] += x[%(a2)s] - x[%(a3)s]; */
  /* a1: {[ii]->[r]: r+-1sigma(inter1(ii))=0} */
  /* a2: {[ii]->[r]: r+-1sigma(inter1(ii))=0} */
  /* a3: {[ii]->[r]: r+-1sigma(inter2(ii))=0} */
  #define S1 fx[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii))] += x[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii))] - x[ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii))];
  /* fx[%(a4)s] += x[%(a5)s] - x[%(a6)s]; */
  /* a4: {[ii]->[r]: r+-1sigma(inter1(ii))=0} */
  /* a5: {[ii]->[r]: r+-1sigma(inter1(ii))=0} */
  /* a6: {[ii]->[r]: r+-1sigma(inter2(ii))=0} */
  #define S2 fx[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii))] += x[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii))] - x[ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii))];

  /* The executor main loop */
  int ii;
  for (ii=0;ii<=n_inter-1;ii++) {
    S1 ;
    S2 ;
  }

  /* Destroy the index array wrappers */
  ER_dtor(&inter1_ER);
  ER_dtor(&inter2_ER);
}
int main()
{
  /* Declare the symbolics */
  int n_inter=10,N=10;

  /* Declare the data spaces */
  double *fx=NULL,*x=NULL;

  /* Declare the index arrays */
  int *inter1=NULL,*inter2=NULL;

  /* Declare pointers for sigma and delta */
  ExplicitRelation *sigma=NULL,*delta=NULL;

  /* Allocate memory for the data spaces */
  fx=(double*)malloc(sizeof(double)*10);
  x=(double*)malloc(sizeof(double)*10);

  /* Allocate memory for the index arrays */
  inter1=(int*)malloc(sizeof(int)*10);
  inter2=(int*)malloc(sizeof(int)*10);

  /* Set index arrays to be 'identity' index arrays */
  for(int i=0;i<10;i++) inter1[i]=i;
  for(int i=0;i<10;i++) inter2[i]=i;

  /* Call the inspector */
  inspector(fx,x,inter1,inter2,n_inter,N,&delta,&sigma);

  /* Call the executor */
  executor(fx,x,inter1,inter2,n_inter,N,&delta,&sigma);

  /* Debug printing of the data arrays */
  for(int i=0;i<10;i++)
  {
    printf("inter1[%d]=%d\n",i,inter1[1]);
    printf("inter2[%d]=%d\n",i,inter1[1]);
    printf("x[%d]=%d\n",i,inter1[1]);
    printf("fx[%d]=%d\n",i,inter1[1]);
  }

  /* Free the data space memory */
  free(fx);
  free(x);

  /* Free the index array memory */
  free(inter1);
  free(inter2);

  return 0;
}
