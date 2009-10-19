void inspector_notrans(int n_inter,int n_moles,int n_tstep,double *data,int *inter1,int *inter2)
{
}

void executor_notrans(int n_inter,int n_moles,int n_tstep,double *data,int *inter1,int *inter2)
{
  ExplicitRelation * inter1_ER;
  ExplicitRelation * inter2_ER;
  int i,ii,tstep;
  inter1_ER=ER_ctor(inter1,n_inter+-1-0);
  inter2_ER=ER_ctor(inter2,n_inter+-1-0);
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
  /* a1: {[tstep,i]->[accessRelation11]: -1i+accessRelation11=0} */
  #define S0(tstep,i) data[ i ][ 3 ] += data[ i ][ 0 ] + data[ i ][ 6 ];
data[ i ][ 4 ] += data[ i ][ 1 ] + data[ i ][ 7 ];
data[ i ][ 5 ] += data[ i ][ 2 ] + data[ i ][ 8 ];
if (data[ i ][ 3 ] < 0.0) data[ i ][ 3 ] += side;
if (data[ i ][ 3 ] > side) data[ i ][ 3 ] -= side;
if (data[ i ][ 4 ] < 0.0) data[ i ][ 4 ] += side;
if (data[ i ][ 4 ] > side) data[ i ][ 4 ] -= side;
if (data[ i ][ 5 ] < 0.0) data[ i ][ 5 ] += side;
if (data[ i ][ 5 ] > side) data[ i ][ 5 ] -= side;
data[ i ][ 0 ] += data[ i ][ 6 ];
data[ i ][ 1 ] += data[ i ][ 7 ];
data[ i ][ 2 ] += data[ i ][ 8 ];
data[ i ][ 6 ] = 0.0;
data[ i ][ 7 ] = 0.0;
data[ i ][ 8 ] = 0.0;
  /* cutoffSquare = cutoffRadius * cutoffRadius;
n_inter = ninter;
vir = 0.0;
epot = 0.0; */
  #define S1(tstep) cutoffSquare = cutoffRadius * cutoffRadius;
n_inter = ninter;
vir = 0.0;
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
  /* a32: {[tstep,ii]->[accessRelation321]: accessRelation321+-1inter2(ii)=0} */
  /* a31: {[tstep,ii]->[accessRelation311]: accessRelation311+-1inter1(ii)=0} */
  #define S2(tstep,ii) xx = data[ ER_out_given_in(inter1_ER,ii) ][ 3 ] - data[ ER_out_given_in(inter2_ER,ii) ][ 3 ];
yy = data[ ER_out_given_in(inter1_ER,ii) ][ 4 ] - data[ ER_out_given_in(inter2_ER,ii) ][ 4 ];
zz = data[ ER_out_given_in(inter1_ER,ii) ][ 5 ] - data[ ER_out_given_in(inter2_ER,ii) ][ 5 ];
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
    data[ ER_out_given_in(inter1_ER,ii) ][ 6 ] += forcex;
    data[ ER_out_given_in(inter1_ER,ii) ][ 7 ] += forcey;
    data[ ER_out_given_in(inter1_ER,ii) ][ 8 ] += forcez;
    data[ ER_out_given_in(inter2_ER,ii) ][ 6 ] -= forcex;
    data[ ER_out_given_in(inter2_ER,ii) ][ 7 ] -= forcey;
    data[ ER_out_given_in(inter2_ER,ii) ][ 8 ] -= forcez;
    vir -= rd * r148;
    epot += (rrd6 - rrd3);
}
  /* data[ %(a43)s ][ 6 ] *= timeStepSqHalf;
data[ %(a43)s ][ 7 ] *= timeStepSqHalf;
data[ %(a43)s ][ 8 ] *= timeStepSqHalf;
data[ %(a43)s ][ 0 ] += data[ %(a43)s ][ 6 ];
data[ %(a43)s ][ 1 ] += data[ %(a43)s ][ 7 ];
data[ %(a43)s ][ 2 ] += data[ %(a43)s ][ 8 ]; */
  /* a43: {[tstep,i]->[accessRelation431]: -1i+accessRelation431=0} */
  #define S3(tstep,i) data[ i ][ 6 ] *= timeStepSqHalf;
data[ i ][ 7 ] *= timeStepSqHalf;
data[ i ][ 8 ] *= timeStepSqHalf;
data[ i ][ 0 ] += data[ i ][ 6 ];
data[ i ][ 1 ] += data[ i ][ 7 ];
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
    if ((n_inter == 0) && (n_moles >= 1)) {
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
    if ((n_inter >= 1) && (n_moles == 0)) {
      for (tstep=0;tstep<=n_tstep-1;tstep++) {
        S1(tstep);
        for (i=0;i<=n_inter-1;i++) {
          S2(tstep,i);
        }
      }
    }
    if ((n_inter == 0) && (n_moles == 0)) {
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

