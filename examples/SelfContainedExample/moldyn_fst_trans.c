void inspector_trans(int N,int T,int n_inter,double *fx,double *x,int *inter1,int *inter2,ExplicitRelation **sigma)
{
  ExplicitRelation * cpack_input_ER;
  ExplicitRelation * sigma_ER;
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,s,i_out0;
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  /* RectUnionDomain for set {[i_out0]: -1i_out0+n_inter+-1>=0 and T+-1>=0 and i_out0>=0 | n_inter,T} */
  /* RectDomain for set {[i_out0]: -1i_out0+n_inter+-1>=0 and T+-1>=0 and i_out0>=0 | n_inter,T} */
  RectDomain *in_domain_cpack_input_conj0=RD_ctor(1);
  RD_set_lb(in_domain_cpack_input_conj0,0,0);
  RD_set_ub(in_domain_cpack_input_conj0,0,n_inter+-1);
  RectUnionDomain *in_domain_cpack_input=RUD_ctor(in_domain_cpack_input_conj0);

  /* Creation of ExplicitRelation of the ARTT */
  /* {[i_out01]->[k2]: k2+-1inter1(i_out01)=0} union {[i_out01]->[k2]: k2+-1inter2(i_out01)=0} */
  cpack_input_ER = ER_ctor(1,1,in_domain_cpack_input,false,false);

  /* Define loop body statements */
  #define S0(i_out01) ER_in_ordered_insert(cpack_input_ER,Tuple_make(i_out01),Tuple_make(ER_out_given_in(inter1_ER,i_out01)));
  #define S1(i_out01) ER_in_ordered_insert(cpack_input_ER,Tuple_make(i_out01),Tuple_make(ER_out_given_in(inter2_ER,i_out01)));

  if ((T >= 1) && (n_inter >= 1)) {
    for (i_out0=0;i_out0<=n_inter-1;i_out0++) {
      S0(i_out0);
      S1(i_out0);
    }
  }

  /* Undefine loop body statements */
  #undef S0
  #undef S1
  /* RectUnionDomain for set {[k]: -1k+N+-1>=0 and k>=0 | N} */
  /* RectDomain for set {[k]: -1k+N+-1>=0 and k>=0 | N} */
  RectDomain *in_domain_sigma_conj0=RD_ctor(1);
  RD_set_lb(in_domain_sigma_conj0,0,0);
  RD_set_ub(in_domain_sigma_conj0,0,N+-1);
  RectUnionDomain *in_domain_sigma=RUD_ctor(in_domain_sigma_conj0);
  *sigma=ER_ctor(1,1,in_domain_sigma,true,true);
  sigma_ER=*sigma;
  ERG_cpack(cpack_input_ER,sigma_ER);
  reorderArray((unsigned char*)x,sizeof(double),N+-1-0,sigma_ER);
  reorderArray((unsigned char*)fx,sizeof(double),N+-1-0,sigma_ER);
}

void executor_trans(int N,int T,int n_inter,double *fx,double *x,int *inter1,int *inter2,ExplicitRelation **sigma)
{
  ExplicitRelation * cpack_input_ER;
  ExplicitRelation * sigma_ER;
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,s,i_out0;
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
  sigma_ER=*sigma;
  /* Define the executor main loop body statments */
  /* x[%(a1)s] = fx[%(a2)s] * 1.25; */
  /* a1: {[s,i]->[sigma_out]: sigma_out+-1sigma(i)=0} */
  /* a2: {[s,i]->[sigma_out]: sigma_out+-1sigma(i)=0} */
  #define S0(s,i) x[ER_out_given_in(sigma_ER,i)] = fx[ER_out_given_in(sigma_ER,i)] * 1.25;
  /* fx[%(a3)s] += x[%(a4)s] - x[%(a5)s]; */
  /* a3: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter1(i))=0} */
  /* a5: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter2(i))=0} */
  /* a4: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter1(i))=0} */
  #define S1(s,i) fx[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,i))] += x[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,i))] - x[ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,i))];
  /* fx[%(a6)s] += x[%(a7)s] - x[%(a8)s]; */
  /* a8: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter2(i))=0} */
  /* a7: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter1(i))=0} */
  /* a6: {[s,i]->[sigma_out1]: sigma_out1+-1sigma(inter2(i))=0} */
  #define S2(s,i) fx[ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,i))] += x[ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,i))] - x[ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,i))];

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

