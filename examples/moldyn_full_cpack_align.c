void inspector_cpack_align(int n_inter,int n_moles,int n_tstep,double data[][9],int * inter1,int * inter2,ExplicitRelation **sigma)
{
  ExplicitRelation * cpack_input_ER;
  ExplicitRelation * sigma_ER;
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,ii,ii_out0,tstep;
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  /* RectUnionDomain for set {[ii_out0]: -1ii_out0+n_inter+-1>=0 and n_tstep+-1>=0 and ii_out0>=0 | n_inter,n_tstep} */
  /* RectDomain for set {[ii_out0]: -1ii_out0+n_inter+-1>=0 and n_tstep+-1>=0 and ii_out0>=0 | n_inter,n_tstep} */
  RectDomain *in_domain_cpack_input_conj0=RD_ctor(1);
  RD_set_lb(in_domain_cpack_input_conj0,0,0);
  RD_set_ub(in_domain_cpack_input_conj0,0,n_inter+-1);
  RectUnionDomain *in_domain_cpack_input=RUD_ctor(in_domain_cpack_input_conj0);

  /* Creation of ExplicitRelation of the ARTT */
  /* {[ii_out0]->[accessRelation1]: accessRelation1+-1inter1(ii_out0)=0} union {[ii_out0]->[accessRelation1]: accessRelation1+-1inter2(ii_out0)=0} */
  cpack_input_ER = ER_ctor(1,1,in_domain_cpack_input,false,false);

  /* Define loop body statements */
  #define S0(ii_out0) ER_in_ordered_insert(cpack_input_ER,Tuple_make(ii_out0),Tuple_make(ER_out_given_in(inter1_ER,ii_out0)));
  #define S1(ii_out0) ER_in_ordered_insert(cpack_input_ER,Tuple_make(ii_out0),Tuple_make(ER_out_given_in(inter2_ER,ii_out0)));

  if ((n_inter >= 1) && (n_tstep >= 1)) {
    for (ii_out0=0;ii_out0<=n_inter-1;ii_out0++) {
      S0(ii_out0);
      S1(ii_out0);
    }
  }

  /* Undefine loop body statements */
  #undef S0
  #undef S1
  /* RectUnionDomain for set {[k]: -1k+n_moles+-1>=0 and k>=0 | n_moles} */
  /* RectDomain for set {[k]: -1k+n_moles+-1>=0 and k>=0 | n_moles} */
  RectDomain *in_domain_sigma_conj0=RD_ctor(1);
  RD_set_lb(in_domain_sigma_conj0,0,0);
  RD_set_ub(in_domain_sigma_conj0,0,n_moles+-1);
  RectUnionDomain *in_domain_sigma=RUD_ctor(in_domain_sigma_conj0);
  *sigma=ER_ctor(1,1,in_domain_sigma,true,true);
  sigma_ER=*sigma;
  ERG_cpack(cpack_input_ER,sigma_ER);
  reorderArray((unsigned char*)data,sizeof(double),n_moles+-1-0,sigma_ER);
}

void executor_cpack_align(int n_inter,int n_moles,int n_tstep,double data[][9],int * inter1,int * inter2,ExplicitRelation **sigma)
{
  ExplicitRelation * cpack_input_ER;
  ExplicitRelation * sigma_ER;
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,ii,ii_out0,tstep;
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
  sigma_ER=*sigma;
  /* Define the executor main loop body statments */
  /* data[ %(a1)s ][ 3 ] += data[ %(a1)s ][ 0 ] + data[ %(a1)s ][ 6 ];
data[ %(a1)s ][ 4 ] += data[ %(a1)s ][ 1 ] + data[ %(a1)s ][ 7 ];
data[ %(a1)s ][ 5 ] += data[ %(a1)s ][ 2 ] + data[ %(a1)s ][ 8 ];
if (data[ %(a1)s ][ 3 ] < 0.0) data[ %(a1)s ][ 3 ] += side;
if (data[ %(a1)s ][ 3 ] > side) data[ %(a1)s ][ 3 ] -= side;
if (data[ %(a1)s ][ 4 ] < 0.0) data[ %(a1)s ][ 4 ] += side;
if (data[ %(a1)s ][ 4 ] > side) data[ %(a1)s ][ 4 ] -= side;
if (data[ %(a1)s ][ 5 ] < 0.0) data[ %(a1)s ][ 5 ] += side;
if (data[ %(a1)s ][ 5 ] > side) data[ %(a1)s ][ 5 ] -= side;
data[ %(a1)s ][ 0 ] += data[ %(a1)s ][ 6 ];
data[ %(a1)s ][ 1 ] += data[ %(a1)s ][ 7 ];
data[ %(a1)s ][ 2 ] += data[ %(a1)s ][ 8 ];
data[ %(a1)s ][ 6 ] = 0.0;
data[ %(a1)s ][ 7 ] = 0.0;
data[ %(a1)s ][ 8 ] = 0.0; */
  /* a1: {[tstep,i]->[sigma_out1]: -1sigma_out1+i=0} */
  #define S0(tstep,i) data[ i ][ 3 ] += data[ i ][ 0 ] + data[ i ][ 6 ];\
data[ i ][ 4 ] += data[ i ][ 1 ] + data[ i ][ 7 ];\
data[ i ][ 5 ] += data[ i ][ 2 ] + data[ i ][ 8 ];\
if (data[ i ][ 3 ] < 0.0) data[ i ][ 3 ] += side;\
if (data[ i ][ 3 ] > side) data[ i ][ 3 ] -= side;\
if (data[ i ][ 4 ] < 0.0) data[ i ][ 4 ] += side;\
if (data[ i ][ 4 ] > side) data[ i ][ 4 ] -= side;\
if (data[ i ][ 5 ] < 0.0) data[ i ][ 5 ] += side;\
if (data[ i ][ 5 ] > side) data[ i ][ 5 ] -= side;\
data[ i ][ 0 ] += data[ i ][ 6 ];\
data[ i ][ 1 ] += data[ i ][ 7 ];\
data[ i ][ 2 ] += data[ i ][ 8 ];\
data[ i ][ 6 ] = 0.0;\
data[ i ][ 7 ] = 0.0;\
data[ i ][ 8 ] = 0.0;
  /* cutoffSquare = cutoffRadius * cutoffRadius;
n_inter = ninter;
vir = 0.0;
epot = 0.0; */
  #define S1(tstep) cutoffSquare = cutoffRadius * cutoffRadius;\
n_inter = ninter;\
vir = 0.0;\
epot = 0.0;
  /* xx = data[ %(a31)s ][ 3 ] - data[ %(a32)s ][ 3 ];
yy = data[ %(a31)s ][ 4 ] - data[ %(a32)s ][ 4 ];
zz = data[ %(a31)s ][ 5 ] - data[ %(a32)s ][ 5 ];
if (xx < -sideHalf) xx += side;
if (yy < -sideHalf) yy += side;
if (zz < -sideHalf) zz += side;
if (xx > sideHalf) xx -= side;
if (yy > sideHalf) yy -= side;
if (zz > sideHalf) zz -= side;
rd = (xx * xx + yy * yy + zz * zz);
if (rd < cutoffSquare) 
{
    rrd = 1.0 / rd;
    rrd2 = rrd * rrd;
    rrd3 = rrd2 * rrd;
    rrd4 = rrd2 * rrd2;
    rrd6 = rrd2 * rrd4;
    rrd7 = rrd6 * rrd;
    r148 = rrd7 - 0.5 * rrd4;
    forcex = xx * r148;
    forcey = yy * r148;
    forcez = zz * r148;
    data[ %(a31)s ][ 6 ] += forcex;
    data[ %(a31)s ][ 7 ] += forcey;
    data[ %(a31)s ][ 8 ] += forcez;
    data[ %(a32)s ][ 6 ] -= forcex;
    data[ %(a32)s ][ 7 ] -= forcey;
    data[ %(a32)s ][ 8 ] -= forcez;
    vir -= rd * r148;
    epot += (rrd6 - rrd3);
} */
  /* a32: {[tstep,ii]->[sigma_out1]: sigma_out1+-1sigma(inter2(ii))=0} */
  /* a31: {[tstep,ii]->[sigma_out1]: sigma_out1+-1sigma(inter1(ii))=0} */
  #define S2(tstep,ii) xx = data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 3 ] - data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 3 ];\
yy = data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 4 ] - data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 4 ];\
zz = data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 5 ] - data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 5 ];\
if (xx < -sideHalf) xx += side;\
if (yy < -sideHalf) yy += side;\
if (zz < -sideHalf) zz += side;\
if (xx > sideHalf) xx -= side;\
if (yy > sideHalf) yy -= side;\
if (zz > sideHalf) zz -= side;\
rd = (xx * xx + yy * yy + zz * zz);\
if (rd < cutoffSquare) \
{\
    rrd = 1.0 / rd;\
    rrd2 = rrd * rrd;\
    rrd3 = rrd2 * rrd;\
    rrd4 = rrd2 * rrd2;\
    rrd6 = rrd2 * rrd4;\
    rrd7 = rrd6 * rrd;\
    r148 = rrd7 - 0.5 * rrd4;\
    forcex = xx * r148;\
    forcey = yy * r148;\
    forcez = zz * r148;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 6 ] += forcex;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 7 ] += forcey;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter1_ER,ii)) ][ 8 ] += forcez;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 6 ] -= forcex;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 7 ] -= forcey;\
    data[ ER_out_given_in(sigma_ER,ER_out_given_in(inter2_ER,ii)) ][ 8 ] -= forcez;\
    vir -= rd * r148;\
    epot += (rrd6 - rrd3);\
}
  /* data[ %(a43)s ][ 6 ] *= timeStepSqHalf;
data[ %(a43)s ][ 7 ] *= timeStepSqHalf;
data[ %(a43)s ][ 8 ] *= timeStepSqHalf;
data[ %(a43)s ][ 0 ] += data[ %(a43)s ][ 6 ];
data[ %(a43)s ][ 1 ] += data[ %(a43)s ][ 7 ];
data[ %(a43)s ][ 2 ] += data[ %(a43)s ][ 8 ]; */
  /* a43: {[tstep,i]->[sigma_out1]: -1sigma_out1+i=0} */
  #define S3(tstep,i) data[ i ][ 6 ] *= timeStepSqHalf;\
data[ i ][ 7 ] *= timeStepSqHalf;\
data[ i ][ 8 ] *= timeStepSqHalf;\
data[ i ][ 0 ] += data[ i ][ 6 ];\
data[ i ][ 1 ] += data[ i ][ 7 ];\
data[ i ][ 2 ] += data[ i ][ 8 ];

  /* The executor main loop */
  if (n_tstep >= 1) {
    if ((n_inter >= 1) && (n_moles >= 1)) {
      for (tstep=0;tstep<=n_tstep-1;tstep++) {
        for (i=0;i<=n_moles-1;i++) {
          S0(tstep,i);
        }
        S1(tstep);
        for (i=0;i<=n_inter-1;i++) {
          S2(tstep,i);
        }
        for (i=0;i<=n_moles-1;i++) {
          S3(tstep,i);
        }
      }
    }
    if ((n_inter <= 0) && (n_moles >= 1)) {
      for (tstep=0;tstep<=n_tstep-1;tstep++) {
        for (i=0;i<=n_moles-1;i++) {
          S0(tstep,i);
        }
        S1(tstep);
        for (i=0;i<=n_moles-1;i++) {
          S3(tstep,i);
        }
      }
    }
    if ((n_inter >= 1) && (n_moles <= 0)) {
      for (tstep=0;tstep<=n_tstep-1;tstep++) {
        S1(tstep);
        for (i=0;i<=n_inter-1;i++) {
          S2(tstep,i);
        }
      }
    }
    if ((n_inter <= 0) && (n_moles <= 0)) {
      for (tstep=0;tstep<=n_tstep-1;tstep++) {
        S1(tstep);
      }
    }
  }

  /* Undefine the executor main loop body statments */
  #undef S0
  #undef S1
  #undef S2
  #undef S3

}

