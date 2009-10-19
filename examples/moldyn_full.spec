# ------------------------------------------------------------------------------
#         Original code:
#         #pragma iegen for       moldyn;
#              #pragma iegen symbolic  n_moles "int %s" 0 INF;
#              #pragma iegen symbolic  n_inter "int %s" 0 INF;
#              #pragma iegen symbolic  n_tstep "int %s" 0 INF;
#              #pragma iegen index     inter1  "int %s[]"         {[k]: 0<=k && k<n_inter} -> {[k]: 0<=k && k<n_moles};
#              #pragma iegen index     inter2  "int %s[]"         {[k]: 0<=k && k<n_inter} -> {[k]: 0<=k && k<n_moles};
#              #pragma iegen data      data    "double %s[][9]"   {[k]: 0<=k && k<n_moles};
#              for (tstep = 0; tstep < n_tstep; tstep++) {
#         
#                 /*................*/
#                 /* UpdateCoordinates(); */
#                 for ( i=0; i<n_moles; i++) {
#         
#                   data[i][3] += data[i][0] + data[i][6];
#                   data[i][4] += data[i][1] + data[i][7];
#                   data[i][5] += data[i][2] + data[i][8];
#         
#                   if ( data[i][3] < 0.0 )  data[i][3] += side ; 
#                   if ( data[i][3] > side ) data[i][3] -= side ;
#                   if ( data[i][4] < 0.0 )  data[i][4] += side ;
#                   if ( data[i][4] > side ) data[i][4] -= side ;
#                   if ( data[i][5] < 0.0 )  data[i][5] += side ;
#                   if ( data[i][5] > side ) data[i][5] -= side ;
#         
#                   data[i][0] += data[i][6];
#                   data[i][1] += data[i][7];
#                   data[i][2] += data[i][8];
#                   data[i][6]  = 0.0;
#                   data[i][7]  = 0.0;
#                   data[i][8]  = 0.0;
#                 }
#         
#                 /*................*/
#                 /* ComputeForces(); */
#         
#                 cutoffSquare = cutoffRadius*cutoffRadius ;
#                 n_inter = ninter;
#                 vir  = 0.0 ;
#                 epot = 0.0;
#         
#                 for(ii=0; ii<n_inter; ii++) {
#                   xx = data[inter1[ii]][3] - data[inter2[ii]][3];
#                   yy = data[inter1[ii]][4] - data[inter2[ii]][4];
#                   zz = data[inter1[ii]][5] - data[inter2[ii]][5];
#         
#                   if (xx < -sideHalf) xx += side;
#                   if (yy < -sideHalf) yy += side;
#                   if (zz < -sideHalf) zz += side;
#                   if (xx > sideHalf) xx -= side;
#                   if (yy > sideHalf) yy -= side;
#                   if (zz > sideHalf) zz -= side;
#                   rd = (xx*xx + yy*yy + zz*zz);
#                   /*if ( 0 ) {*/
#                   if ( rd < cutoffSquare ) {
#                     rrd   = 1.0/rd;
#                     rrd2  = rrd*rrd ;
#                     rrd3  = rrd2*rrd ;
#                     rrd4  = rrd2*rrd2 ;
#                     rrd6  = rrd2*rrd4;
#                     rrd7  = rrd6*rrd ;
#                     r148  = rrd7 - 0.5 * rrd4 ;
#         
#                     forcex = xx*r148;
#                     forcey = yy*r148;
#                     forcez = zz*r148;
#         
#                     data[inter1[ii]][6]  += forcex ;
#                     data[inter1[ii]][7]  += forcey ;
#                     data[inter1[ii]][8]  += forcez ;
#         
#                     data[inter2[ii]][6]  -= forcex ;
#                     data[inter2[ii]][7]  -= forcey ;
#                     data[inter2[ii]][8]  -= forcez ;
#         
#                     vir  -= rd*r148 ;
#                     epot += (rrd6 - rrd3);
#                   }
#                 }
#         
#                 /*................*/
#                 /* UpdateVelocities(); */
#                 for ( i = 0; i< n_moles; i++) {
#                   data[i][6]  *= timeStepSqHalf ;
#                   data[i][7]  *= timeStepSqHalf ;
#                   data[i][8]  *= timeStepSqHalf ;
#                   data[i][0]  += data[i][6];
#                   data[i][1]  += data[i][7];
#                   data[i][2]  += data[i][8];
#                 }
#         
#               } /* end of time stepping loop */
#               #pragma iegen endfor
# ------------------------------------------------------------------------------


spec.add_symbolic(name='n_inter',type='int %s')

spec.add_symbolic(name='n_tstep',type='int %s')

spec.add_symbolic(name='n_moles',type='int %s')


spec.add_data_array(
        name='data',
        type='double %s[][9]',
        bounds='{[k]: 0<=k && k<n_moles}')

spec.add_index_array(
        name='inter1',
        type='int * %s',
        input_bounds='{[k]: 0<=k && k<n_inter}',
        output_bounds='{[k]: 0<=k && k<n_moles}')

spec.add_index_array(
        name='inter2',
        type='int * %s',
        input_bounds='{[k]: 0<=k && k<n_inter}',
        output_bounds='{[k]: 0<=k && k<n_moles}')

# ------------------------------------------------------------------------------
#         Line 270: data[i][3] += data[i][0] + data[i][6];
#         Line 271: data[i][4] += data[i][1] + data[i][7];
#         Line 272: data[i][5] += data[i][2] + data[i][8];
#         Line 274: if ( data[i][3] < 0.0 )  data[i][3] += side ;
#         Line 275: if ( data[i][3] > side ) data[i][3] -= side ;
#         Line 276: if ( data[i][4] < 0.0 )  data[i][4] += side ;
#         Line 277: if ( data[i][4] > side ) data[i][4] -= side ;
#         Line 278: if ( data[i][5] < 0.0 )  data[i][5] += side ;
#         Line 279: if ( data[i][5] > side ) data[i][5] -= side ;
#         Line 281: data[i][0] += data[i][6];
#         Line 282: data[i][1] += data[i][7];
#         Line 283: data[i][2] += data[i][8];
#         Line 284: data[i][6]  = 0.0;
#         Line 285: data[i][7]  = 0.0;
#         Line 286: data[i][8]  = 0.0;
# ------------------------------------------------------------------------------

spec.add_statement(
        name='s__0_tstep_0_i_0',
        text='''data[ %(a1)s ][ 3 ] += data[ %(a1)s ][ 0 ] + data[ %(a1)s ][ 6 ];
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
data[ %(a1)s ][ 8 ] = 0.0;''',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c0, i, c0 ] : c0=0 }')
spec.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a1',
        data_array='data',
        iter_to_data='{ [tstep, i]->[accessRelation1] : accessRelation1 = i }')


# ------------------------------------------------------------------------------
#         Line 292: cutoffSquare = cutoffRadius*cutoffRadius ;
#         Line 293: n_inter = ninter;
#         Line 294: vir  = 0.0 ;
#         Line 295: epot = 0.0;
# ------------------------------------------------------------------------------

spec.add_statement(
        name='s__0_tstep_1',
        text='''cutoffSquare = cutoffRadius * cutoffRadius;
n_inter = ninter;
vir = 0.0;
epot = 0.0;''',
        iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
        scatter='{ [ tstep ]->[ c0, tstep, c1, c0, c0 ] : c0=0 && c1=1 }')


# ------------------------------------------------------------------------------
#         Line 298: xx = data[inter1[ii]][3] - data[inter2[ii]][3];
#         Line 299: yy = data[inter1[ii]][4] - data[inter2[ii]][4];
#         Line 300: zz = data[inter1[ii]][5] - data[inter2[ii]][5];
#         Line 302: if (xx < -sideHalf) xx += side;
#         Line 303: if (yy < -sideHalf) yy += side;
#         Line 304: if (zz < -sideHalf) zz += side;
#         Line 305: if (xx > sideHalf) xx -= side;
#         Line 306: if (yy > sideHalf) yy -= side;
#         Line 307: if (zz > sideHalf) zz -= side;
#         Line 308: rd = (xx*xx + yy*yy + zz*zz);
#         Line 310: if ( rd < cutoffSquare ) {
# ------------------------------------------------------------------------------

spec.add_statement(
        name='s__0_tstep_5_ii_0',
        text='''xx = data[ %(a31)s ][ 3 ] - data[ %(a32)s ][ 3 ];
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
}''',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c2, ii, c0 ] : c0=0 && c2=2 }')
spec.add_access_relation(
        statement_name='s__0_tstep_5_ii_0',
        name='a31',
        data_array='data',
        iter_to_data='{ [tstep, ii]->[accessRelation31] : accessRelation31 = inter1(ii) }')
spec.add_access_relation(
        statement_name='s__0_tstep_5_ii_0',
        name='a32',
        data_array='data',
        iter_to_data='{ [tstep, ii]->[accessRelation32] : accessRelation32 = inter2(ii) }')

# ------------------------------------------------------------------------------
#         Line 339: data[i][6]  *= timeStepSqHalf ;
#         Line 340: data[i][7]  *= timeStepSqHalf ;
#         Line 341: data[i][8]  *= timeStepSqHalf ;
#         Line 342: data[i][0]  += data[i][6];
#         Line 343: data[i][1]  += data[i][7];
#         Line 344: data[i][2]  += data[i][8];
# ------------------------------------------------------------------------------

spec.add_statement(
        name='s__0_tstep_6_i_0',
        text='''data[ %(a43)s ][ 6 ] *= timeStepSqHalf;
data[ %(a43)s ][ 7 ] *= timeStepSqHalf;
data[ %(a43)s ][ 8 ] *= timeStepSqHalf;
data[ %(a43)s ][ 0 ] += data[ %(a43)s ][ 6 ];
data[ %(a43)s ][ 1 ] += data[ %(a43)s ][ 7 ];
data[ %(a43)s ][ 2 ] += data[ %(a43)s ][ 8 ];''',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c3, i, c0 ] : c0=0 && c3=3 }')
spec.add_access_relation(
        statement_name='s__0_tstep_6_i_0',
        name='a43',
        data_array='data',
        iter_to_data='{ [tstep, i]->[accessRelation43] : accessRelation43 = i }')
