#!/usr/bin/env python

import iegen,iegen.trans

moldyn=iegen.MapIR()

moldyn.add_symbolic(name='n_moles')

moldyn.add_symbolic(name='n_tstep')

moldyn.add_symbolic(name='n_inter')

syms=moldyn.get_symbolics()

moldyn.add_data_array(
        name='x',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='fx',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='vhy',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='y',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='vhx',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='fz',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='z',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='vhz',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_data_array(
        name='fy',
        bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_index_array(
        name='inter1',
        input_bounds='{[k]: 0<=k && k<n_inter}',
        output_bounds='{[k]: 0<=k && k<n_moles}')

moldyn.add_index_array(
        name='inter2',
        input_bounds='{[k]: 0<=k && k<n_inter}',
        output_bounds='{[k]: 0<=k && k<n_moles}')

######
#Line 276: x(i) += vhx(i) + fx(i); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_0_i_0',
        text='x( %(a1)s ) += vhx( %(a2)s ) + fx( %(a3)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=0 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a1',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation1 ] : accessRelation1 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a2',
        data_array='vhx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation2 ] : accessRelation2 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a3',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation3 ] : accessRelation3 = i }')


######
#Line 277: y(i) += vhy(i) + fy(i); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_0_i_1',
        text='y( %(a4)s ) += vhy( %(a5)s ) + fy( %(a6)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=1 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_1',
        name='a4',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation4 ] : accessRelation4 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_1',
        name='a5',
        data_array='vhy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation5 ] : accessRelation5 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_1',
        name='a6',
        data_array='fy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation6 ] : accessRelation6 = i }')


######
#Line 278: z(i) += vhz(i) + fz(i); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_0_i_2',
        text='z( %(a7)s ) += vhz( %(a8)s ) + fz( %(a9)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=2 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_2',
        name='a7',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation7 ] : accessRelation7 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_2',
        name='a8',
        data_array='vhz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation8 ] : accessRelation8 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_2',
        name='a9',
        data_array='fz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation9 ] : accessRelation9 = i }')


######
#Line 280: x(i) = (x(i) + side) * (x(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( x(i) < 0.0 )  x(i) = x(i) + side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_3',
        text='x( %(a10)s ) = ( x( %(a11)s ) + side ) * ( x( %(a12)s ) < 0.0 ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=3 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_3',
        name='a10',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation10 ] : accessRelation10 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_3',
        name='a11',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation11 ] : accessRelation11 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_3',
        name='a12',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation12 ] : accessRelation12 = i }')


######
#Line 281: x(i) = (x(i) - side) * (x(i) > side ? 1 : 0); // ^jroelofs if ( x(i) > side ) x(i) = x(i) - side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_4',
        text='x( %(a13)s ) = ( x( %(a14)s ) - side ) * ( x( %(a15)s ) > side ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=4 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_4',
        name='a13',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation13 ] : accessRelation13 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_4',
        name='a14',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation14 ] : accessRelation14 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_4',
        name='a15',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation15 ] : accessRelation15 = i }')


######
#Line 282: y(i) = (y(i) + side) * (y(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( y(i) < 0.0 )  y(i) = y(i) + side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_5',
        text='y( %(a16)s ) = ( y( %(a17)s ) + side ) * ( y( %(a18)s ) < 0.0 ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=5 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_5',
        name='a16',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation16 ] : accessRelation16 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_5',
        name='a17',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation17 ] : accessRelation17 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_5',
        name='a18',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation18 ] : accessRelation18 = i }')


######
#Line 283: y(i) = (y(i) - side) * (y(i) > side ? 1 : 0); // ^jroelofs if ( y(i) > side ) y(i) = y(i) - side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_6',
        text='y( %(a19)s ) = ( y( %(a20)s ) - side ) * ( y( %(a21)s ) > side ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=6 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_6',
        name='a19',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation19 ] : accessRelation19 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_6',
        name='a20',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation20 ] : accessRelation20 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_6',
        name='a21',
        data_array='y',
        iter_to_data='{ [ tstep, i ]->[ accessRelation21 ] : accessRelation21 = i }')


######
#Line 284: z(i) = (z(i) + side) * (z(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( z(i) < 0.0 )  z(i) = z(i) + side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_7',
        text='z( %(a22)s ) = ( z( %(a23)s ) + side ) * ( z( %(a24)s ) < 0.0 ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=7 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_7',
        name='a22',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation22 ] : accessRelation22 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_7',
        name='a23',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation23 ] : accessRelation23 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_7',
        name='a24',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation24 ] : accessRelation24 = i }')


######
#Line 285: z(i) = (z(i) - side) * (z(i) > side ? 1 : 0); // ^jroelofs if ( z(i) > side ) z(i) = z(i) - side ;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_8',
        text='z( %(a25)s ) = ( z( %(a26)s ) - side ) * ( z( %(a27)s ) > side ? 1 : 0 )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=8 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_8',
        name='a25',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation25 ] : accessRelation25 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_8',
        name='a26',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation26 ] : accessRelation26 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_8',
        name='a27',
        data_array='z',
        iter_to_data='{ [ tstep, i ]->[ accessRelation27 ] : accessRelation27 = i }')


######
#Line 287: vhx(i) = vhx(i) + fx(i);
######
moldyn.add_statement(
        name='s__0_tstep_0_i_9',
        text='vhx( %(a28)s ) = vhx( %(a29)s ) + fx( %(a30)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=9 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_9',
        name='a28',
        data_array='vhx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation28 ] : accessRelation28 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_9',
        name='a29',
        data_array='vhx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation29 ] : accessRelation29 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_9',
        name='a30',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation30 ] : accessRelation30 = i }')


######
#Line 288: vhy(i) = vhy(i) + fy(i);
######
moldyn.add_statement(
        name='s__0_tstep_0_i_10',
        text='vhy( %(a31)s ) = vhy( %(a32)s ) + fy( %(a33)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=10 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_10',
        name='a31',
        data_array='vhy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation31 ] : accessRelation31 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_10',
        name='a32',
        data_array='vhy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation32 ] : accessRelation32 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_10',
        name='a33',
        data_array='fy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation33 ] : accessRelation33 = i }')


######
#Line 289: vhz(i) = vhz(i) + fz(i);
######
moldyn.add_statement(
        name='s__0_tstep_0_i_11',
        text='vhz( %(a34)s ) = vhz( %(a35)s ) + fz( %(a36)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=11 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_11',
        name='a34',
        data_array='vhz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation34 ] : accessRelation34 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_11',
        name='a35',
        data_array='vhz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation35 ] : accessRelation35 = i }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_11',
        name='a36',
        data_array='fz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation36 ] : accessRelation36 = i }')


######
#Line 290: fx(i)  = 0.0;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_12',
        text='fx( %(a37)s ) = 0.0',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=12 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_12',
        name='a37',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation37 ] : accessRelation37 = i }')


######
#Line 291: fy(i)  = 0.0;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_13',
        text='fy( %(a38)s ) = 0.0',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=13 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_13',
        name='a38',
        data_array='fy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation38 ] : accessRelation38 = i }')


######
#Line 292: fz(i)  = 0.0;
######
moldyn.add_statement(
        name='s__0_tstep_0_i_14',
        text='fz( %(a39)s ) = 0.0',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=14 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_0_i_14',
        name='a39',
        data_array='fz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation39 ] : accessRelation39 = i }')


######
#Line 299: cutoffSquare = cutoffRadius*cutoffRadius ;
######
moldyn.add_statement(
        name='s__0_tstep_1',
        text='cutoffSquare = cutoffRadius * cutoffRadius',
        iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
        scatter='{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=1 && t0=0 && c2=0 }')


######
#Line 300: n_inter = ninter;
######
moldyn.add_statement(
        name='s__0_tstep_2',
        text='n_inter = ninter',
        iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
        scatter='{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=2 && t0=0 && c2=0 }')


######
#Line 301: vir  = 0.0 ;
######
moldyn.add_statement(
        name='s__0_tstep_3',
        text='vir = 0.0',
        iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
        scatter='{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=3 && t0=0 && c2=0 }')


######
#Line 302: epot = 0.0;
######
moldyn.add_statement(
        name='s__0_tstep_4',
        text='epot = 0.0',
        iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
        scatter='{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=4 && t0=0 && c2=0 }')


######
#Line 309: xx = x(inter1(ii) - x(inter2(ii);
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_0',
        text='xx = x( %(a40)s ) - x( %(a41)s )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=0 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_0',
        name='a40',
        data_array='x',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation40 ] : accessRelation40 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_0',
        name='a41',
        data_array='x',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation41 ] : accessRelation41 = inter2( ii ) }')


######
#Line 310: yy = y(inter1(ii) - y(inter2(ii);
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_1',
        text='yy = y( %(a42)s ) - y( %(a43)s )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=1 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_1',
        name='a42',
        data_array='y',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation42 ] : accessRelation42 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_1',
        name='a43',
        data_array='y',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation43 ] : accessRelation43 = inter2( ii ) }')


######
#Line 311: zz = z(inter1(ii) - z(inter2(ii);
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_2',
        text='zz = z( %(a44)s ) - z( %(a45)s )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=2 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_2',
        name='a44',
        data_array='z',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation44 ] : accessRelation44 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_2',
        name='a45',
        data_array='z',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation45 ] : accessRelation45 = inter2( ii ) }')


######
#Line 313: xx += side * (xx < -sideHalf ? 1 : 0); // ^jroelofs if (xx < -sideHalf) xx += side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_3',
        text='xx += side * ( xx < -sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=3 }')


######
#Line 314: yy += side * (yy < -sideHalf ? 1 : 0); // ^jroelofs if (yy < -sideHalf) yy += side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_4',
        text='yy += side * ( yy < -sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=4 }')


######
#Line 315: zz += side * (zz < -sideHalf ? 1 : 0); // ^jroelofs if (zz < -sideHalf) zz += side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_5',
        text='zz += side * ( zz < -sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=5 }')


######
#Line 316: xx -= side * (xx > sideHalf ? 1 : 0);  // ^jroelofs if (xx > sideHalf) xx -= side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_6',
        text='xx -= side * ( xx > sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=6 }')


######
#Line 317: yy -= side * (yy > sideHalf ? 1 : 0);  // ^jroelofs if (yy > sideHalf) yy -= side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_7',
        text='yy -= side * ( yy > sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=7 }')


######
#Line 318: zz -= side * (zz > sideHalf ? 1 : 0);  // ^jroelofs if (zz > sideHalf) zz -= side;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_8',
        text='zz -= side * ( zz > sideHalf ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=8 }')


######
#Line 319: rd = (xx*xx + yy*yy + zz*zz);
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_9',
        text='rd = ( xx * xx + yy * yy + zz * zz )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=9 }')


######
#Line 323: rd_lt_cutoffSquare = (rd < cutoffSquare ? 1 : 0); // +jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_10',
        text='rd_lt_cutoffSquare = ( rd < cutoffSquare ? 1 : 0 )',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=10 }')


######
#Line 325: rrd   = 1.0/rd;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_11',
        text='rrd = 1.0 / rd',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=11 }')


######
#Line 326: rrd2  = rrd*rrd ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_12',
        text='rrd2 = rrd * rrd',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=12 }')


######
#Line 327: rrd3  = rrd2*rrd ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_13',
        text='rrd3 = rrd2 * rrd',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=13 }')


######
#Line 328: rrd4  = rrd2*rrd2 ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_14',
        text='rrd4 = rrd2 * rrd2',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=14 }')


######
#Line 329: rrd6  = rrd2*rrd4;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_15',
        text='rrd6 = rrd2 * rrd4',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=15 }')


######
#Line 330: rrd7  = rrd6*rrd ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_16',
        text='rrd7 = rrd6 * rrd',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=16 }')


######
#Line 331: r148  = rrd7 - 0.5 * rrd4 ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_17',
        text='r148 = rrd7 - 0.5 * rrd4',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=17 }')


######
#Line 333: forcex = xx*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_18',
        text='forcex = xx * r148 * rd_lt_cutoffSquare',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=18 }')


######
#Line 334: forcey = yy*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_19',
        text='forcey = yy * r148 * rd_lt_cutoffSquare',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=19 }')


######
#Line 335: forcez = zz*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_20',
        text='forcez = zz * r148 * rd_lt_cutoffSquare',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=20 }')


######
#Line 337: fx(inter1(ii)  += forcex ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_21',
        text='fx( %(a46)s ) += forcex',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=21 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_21',
        name='a46',
        data_array='fx',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation46 ] : accessRelation46 = inter1( ii ) }')


######
#Line 338: fy(inter1(ii)  += forcey ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_22',
        text='fy( %(a47)s ) += forcey',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=22 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_22',
        name='a47',
        data_array='fy',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation47 ] : accessRelation47 = inter1( ii ) }')


######
#Line 339: fz(inter1(ii)  += forcez ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_23',
        text='fz( %(a48)s ) += forcez',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=23 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_23',
        name='a48',
        data_array='fz',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation48 ] : accessRelation48 = inter1( ii ) }')


######
#Line 341: fx(inter2(ii)  -= forcex ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_24',
        text='fx( %(a49)s ) -= forcex',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=24 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_24',
        name='a49',
        data_array='fx',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation49 ] : accessRelation49 = inter2( ii ) }')


######
#Line 342: fy(inter2(ii)  -= forcey ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_25',
        text='fy( %(a50)s ) -= forcey',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=25 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_25',
        name='a50',
        data_array='fy',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation50 ] : accessRelation50 = inter2( ii ) }')


######
#Line 343: fz(inter2(ii)  -= forcez ;
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_26',
        text='fz( %(a51)s ) -= forcez',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=26 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_5_ii_26',
        name='a51',
        data_array='fz',
        iter_to_data='{ [ tstep, ii ]->[ accessRelation51 ] : accessRelation51 = inter2( ii ) }')


######
#Line 345: vir  -= rd*r148 * rd_lt_cutoffSquare; // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_27',
        text='vir -= rd * r148 * rd_lt_cutoffSquare',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=27 }')


######
#Line 346: epot += (rrd6 - rrd3) * rd_lt_cutoffSquare; // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_5_ii_28',
        text='epot += ( rrd6 - rrd3 ) * rd_lt_cutoffSquare',
        iter_space='{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }',
        scatter='{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=28 }')


######
#Line 352: fx(inter1(ii) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_0',
        text='fx( %(a52)s ) *= timeStepSqHalf',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=0 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_0',
        name='a52',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation52 ] : accessRelation52 = inter1( ii ) }')


######
#Line 353: fy(inter1(ii) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_1',
        text='fy( %(a53)s ) *= timeStepSqHalf',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=1 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_1',
        name='a53',
        data_array='fy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation53 ] : accessRelation53 = inter1( ii ) }')


######
#Line 354: fz(inter1(ii) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_2',
        text='fz( %(a54)s ) *= timeStepSqHalf',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=2 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_2',
        name='a54',
        data_array='fz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation54 ] : accessRelation54 = inter1( ii ) }')


######
#Line 355: vhx(inter1(ii) += fx(inter1(ii); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_3',
        text='vhx( %(a55)s ) += fx( %(a56)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=3 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_3',
        name='a55',
        data_array='vhx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation55 ] : accessRelation55 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_3',
        name='a56',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation56 ] : accessRelation56 = inter1( ii ) }')


######
#Line 356: vhy(inter1(ii) += fy(inter1(ii); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_4',
        text='vhy( %(a57)s ) += fy( %(a58)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=4 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_4',
        name='a57',
        data_array='vhy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation57 ] : accessRelation57 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_4',
        name='a58',
        data_array='fy',
        iter_to_data='{ [ tstep, i ]->[ accessRelation58 ] : accessRelation58 = inter1( ii ) }')


######
#Line 357: vhz(inter1(ii) += fz(inter1(ii); // ^jroelofs
######
moldyn.add_statement(
        name='s__0_tstep_6_i_5',
        text='vhz( %(a59)s ) += fz( %(a60)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=5 }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_5',
        name='a59',
        data_array='vhz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation59 ] : accessRelation59 = inter1( ii ) }')
moldyn.add_access_relation(
        statement_name='s__0_tstep_6_i_5',
        name='a60',
        data_array='fz',
        iter_to_data='{ [ tstep, i ]->[ accessRelation60 ] : accessRelation60 = inter1( ii ) }')

moldyn.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['x','fx'],
    iter_sub_space_relation='{[c0,tstep,c1,i,c2]->[i]: c1=1}',
    target_data_array='x',
    erg_func_name='ERG_cpack')

print moldyn.codegen('iegen_moldyn_ouput.c')
