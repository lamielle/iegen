void inspector_notrans(int N,int T,int n_inter,double *fx,double *x,int *inter1,int *inter2)
{
}

void executor_notrans(int N,int T,int n_inter,double *fx,double *x,int *inter1,int *inter2)
{
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,s;
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
  /* Define the executor main loop body statments */
  /* x[%(a1)s] = fx[%(a2)s] * 1.25; */
  /* a1: {[s,i]->[i_out01]: -1i_out01+i=0} */
  /* a2: {[s,i]->[i_out01]: -1i_out01+i=0} */
  #define S0(s,i) x[i] = fx[i] * 1.25;
  /* fx[%(a3)s] += x[%(a4)s] - x[%(a5)s]; */
  /* a3: {[s,i]->[k1]: k1+-1inter1(i)=0} */
  /* a5: {[s,i]->[k1]: k1+-1inter2(i)=0} */
  /* a4: {[s,i]->[k1]: k1+-1inter1(i)=0} */
  #define S1(s,i) fx[ER_out_given_in(inter1_ER,i)] += x[ER_out_given_in(inter1_ER,i)] - x[ER_out_given_in(inter2_ER,i)];
  /* fx[%(a6)s] += x[%(a7)s] - x[%(a8)s]; */
  /* a8: {[s,i]->[k1]: k1+-1inter2(i)=0} */
  /* a7: {[s,i]->[k1]: k1+-1inter1(i)=0} */
  /* a6: {[s,i]->[k1]: k1+-1inter2(i)=0} */
  #define S2(s,i) fx[ER_out_given_in(inter2_ER,i)] += x[ER_out_given_in(inter1_ER,i)] - x[ER_out_given_in(inter2_ER,i)];

  /* The executor main loop */
  if ((T >= 1) && (n_inter >= -N+1)) {
    if ((N >= 1) && (n_inter >= 1)) {
      for (s=0;s<=T-1;s++) {
        for (i=0;i<=N-1;i++) {
          S0(s,i);
        }
        for (i=0;i<=n_inter-1;i++) {
          S1(s,i);
          S2(s,i);
        }
      }
    }
    if (n_inter == 0) {
      for (s=0;s<=T-1;s++) {
        for (i=0;i<=N-1;i++) {
          S0(s,i);
        }
      }
    }
    if (N == 0) {
      for (s=0;s<=T-1;s++) {
        for (i=0;i<=n_inter-1;i++) {
          S1(s,i);
          S2(s,i);
        }
      }
    }
  }

  /* Undefine the executor main loop body statments */
  #undef S0
  #undef S1
  #undef S2

}

