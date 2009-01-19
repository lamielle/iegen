#!/usr/bin/env python

from iegen import MapIR,Symbolic,DataArray,IndexArray,Statement,AccessRelation,Set,Relation
from iegen.trans import DataPermuteTrans,IterPermuteTrans

moldyn=MapIR()

moldyn.add_symbolic(Symbolic('n_moles'))

moldyn.add_symbolic(Symbolic('n_tstep'))

moldyn.add_symbolic(Symbolic('n_inter'))

syms=moldyn.get_symbolics()

moldyn.add_data_array(DataArray(
        name='x',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='fx',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='vhy',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='y',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='vhx',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='fz',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='z',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='vhz',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_data_array(DataArray(
        name='fy',
        bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_index_array(IndexArray(
        name='inter1',
        input_bounds=Set('{[k]: 0<=k && k<n_inter}', syms),
        output_bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

moldyn.add_index_array(IndexArray(
        name='inter2',
        input_bounds=Set('{[k]: 0<=k && k<n_inter}', syms),
        output_bounds=Set('{[k]: 0<=k && k<n_moles}', syms)))

######
#Line 276: x(i) += vhx(i) + fx(i); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_0',
        text='x( %(a1)s ) += vhx( %(a2)s ) + fx( %(a3)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=0 }', syms)))
moldyn.statements['s__0_tstep_0_i_0'].add_access_relation(AccessRelation(
        name='a1',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation1 ] : accessRelation1 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_0'].add_access_relation(AccessRelation(
        name='a2',
        data_array=moldyn.data_arrays['vhx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation2 ] : accessRelation2 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_0'].add_access_relation(AccessRelation(
        name='a3',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation3 ] : accessRelation3 = i }', syms)))


######
#Line 277: y(i) += vhy(i) + fy(i); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_1',
        text='y( %(a4)s ) += vhy( %(a5)s ) + fy( %(a6)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=1 }', syms)))
moldyn.statements['s__0_tstep_0_i_1'].add_access_relation(AccessRelation(
        name='a4',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation4 ] : accessRelation4 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_1'].add_access_relation(AccessRelation(
        name='a5',
        data_array=moldyn.data_arrays['vhy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation5 ] : accessRelation5 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_1'].add_access_relation(AccessRelation(
        name='a6',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation6 ] : accessRelation6 = i }', syms)))


######
#Line 278: z(i) += vhz(i) + fz(i); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_2',
        text='z( %(a7)s ) += vhz( %(a8)s ) + fz( %(a9)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=2 }', syms)))
moldyn.statements['s__0_tstep_0_i_2'].add_access_relation(AccessRelation(
        name='a7',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation7 ] : accessRelation7 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_2'].add_access_relation(AccessRelation(
        name='a8',
        data_array=moldyn.data_arrays['vhz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation8 ] : accessRelation8 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_2'].add_access_relation(AccessRelation(
        name='a9',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation9 ] : accessRelation9 = i }', syms)))


######
#Line 280: x(i) = (x(i) + side) * (x(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( x(i) < 0.0 )  x(i) = x(i) + side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_3',
        text='x( %(a10)s ) = ( x( %(a11)s ) + side ) * ( x( %(a12)s ) < 0.0 ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=3 }', syms)))
moldyn.statements['s__0_tstep_0_i_3'].add_access_relation(AccessRelation(
        name='a10',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation10 ] : accessRelation10 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_3'].add_access_relation(AccessRelation(
        name='a11',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation11 ] : accessRelation11 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_3'].add_access_relation(AccessRelation(
        name='a12',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation12 ] : accessRelation12 = i }', syms)))


######
#Line 281: x(i) = (x(i) - side) * (x(i) > side ? 1 : 0); // ^jroelofs if ( x(i) > side ) x(i) = x(i) - side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_4',
        text='x( %(a13)s ) = ( x( %(a14)s ) - side ) * ( x( %(a15)s ) > side ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=4 }', syms)))
moldyn.statements['s__0_tstep_0_i_4'].add_access_relation(AccessRelation(
        name='a13',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation13 ] : accessRelation13 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_4'].add_access_relation(AccessRelation(
        name='a14',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation14 ] : accessRelation14 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_4'].add_access_relation(AccessRelation(
        name='a15',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation15 ] : accessRelation15 = i }', syms)))


######
#Line 282: y(i) = (y(i) + side) * (y(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( y(i) < 0.0 )  y(i) = y(i) + side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_5',
        text='y( %(a16)s ) = ( y( %(a17)s ) + side ) * ( y( %(a18)s ) < 0.0 ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=5 }', syms)))
moldyn.statements['s__0_tstep_0_i_5'].add_access_relation(AccessRelation(
        name='a16',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation16 ] : accessRelation16 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_5'].add_access_relation(AccessRelation(
        name='a17',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation17 ] : accessRelation17 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_5'].add_access_relation(AccessRelation(
        name='a18',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation18 ] : accessRelation18 = i }', syms)))


######
#Line 283: y(i) = (y(i) - side) * (y(i) > side ? 1 : 0); // ^jroelofs if ( y(i) > side ) y(i) = y(i) - side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_6',
        text='y( %(a19)s ) = ( y( %(a20)s ) - side ) * ( y( %(a21)s ) > side ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=6 }', syms)))
moldyn.statements['s__0_tstep_0_i_6'].add_access_relation(AccessRelation(
        name='a19',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation19 ] : accessRelation19 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_6'].add_access_relation(AccessRelation(
        name='a20',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation20 ] : accessRelation20 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_6'].add_access_relation(AccessRelation(
        name='a21',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation21 ] : accessRelation21 = i }', syms)))


######
#Line 284: z(i) = (z(i) + side) * (z(i) < 0.0 ? 1 : 0);  // ^jroelofs if ( z(i) < 0.0 )  z(i) = z(i) + side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_7',
        text='z( %(a22)s ) = ( z( %(a23)s ) + side ) * ( z( %(a24)s ) < 0.0 ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=7 }', syms)))
moldyn.statements['s__0_tstep_0_i_7'].add_access_relation(AccessRelation(
        name='a22',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation22 ] : accessRelation22 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_7'].add_access_relation(AccessRelation(
        name='a23',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation23 ] : accessRelation23 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_7'].add_access_relation(AccessRelation(
        name='a24',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation24 ] : accessRelation24 = i }', syms)))


######
#Line 285: z(i) = (z(i) - side) * (z(i) > side ? 1 : 0); // ^jroelofs if ( z(i) > side ) z(i) = z(i) - side ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_8',
        text='z( %(a25)s ) = ( z( %(a26)s ) - side ) * ( z( %(a27)s ) > side ? 1 : 0 )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=8 }', syms)))
moldyn.statements['s__0_tstep_0_i_8'].add_access_relation(AccessRelation(
        name='a25',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation25 ] : accessRelation25 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_8'].add_access_relation(AccessRelation(
        name='a26',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation26 ] : accessRelation26 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_8'].add_access_relation(AccessRelation(
        name='a27',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation27 ] : accessRelation27 = i }', syms)))


######
#Line 287: vhx(i) = vhx(i) + fx(i);
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_9',
        text='vhx( %(a28)s ) = vhx( %(a29)s ) + fx( %(a30)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=9 }', syms)))
moldyn.statements['s__0_tstep_0_i_9'].add_access_relation(AccessRelation(
        name='a28',
        data_array=moldyn.data_arrays['vhx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation28 ] : accessRelation28 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_9'].add_access_relation(AccessRelation(
        name='a29',
        data_array=moldyn.data_arrays['vhx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation29 ] : accessRelation29 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_9'].add_access_relation(AccessRelation(
        name='a30',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation30 ] : accessRelation30 = i }', syms)))


######
#Line 288: vhy(i) = vhy(i) + fy(i);
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_10',
        text='vhy( %(a31)s ) = vhy( %(a32)s ) + fy( %(a33)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=10 }', syms)))
moldyn.statements['s__0_tstep_0_i_10'].add_access_relation(AccessRelation(
        name='a31',
        data_array=moldyn.data_arrays['vhy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation31 ] : accessRelation31 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_10'].add_access_relation(AccessRelation(
        name='a32',
        data_array=moldyn.data_arrays['vhy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation32 ] : accessRelation32 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_10'].add_access_relation(AccessRelation(
        name='a33',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation33 ] : accessRelation33 = i }', syms)))


######
#Line 289: vhz(i) = vhz(i) + fz(i);
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_11',
        text='vhz( %(a34)s ) = vhz( %(a35)s ) + fz( %(a36)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=11 }', syms)))
moldyn.statements['s__0_tstep_0_i_11'].add_access_relation(AccessRelation(
        name='a34',
        data_array=moldyn.data_arrays['vhz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation34 ] : accessRelation34 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_11'].add_access_relation(AccessRelation(
        name='a35',
        data_array=moldyn.data_arrays['vhz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation35 ] : accessRelation35 = i }', syms)))
moldyn.statements['s__0_tstep_0_i_11'].add_access_relation(AccessRelation(
        name='a36',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation36 ] : accessRelation36 = i }', syms)))


######
#Line 290: fx(i)  = 0.0;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_12',
        text='fx( %(a37)s ) = 0.0',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=12 }', syms)))
moldyn.statements['s__0_tstep_0_i_12'].add_access_relation(AccessRelation(
        name='a37',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation37 ] : accessRelation37 = i }', syms)))


######
#Line 291: fy(i)  = 0.0;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_13',
        text='fy( %(a38)s ) = 0.0',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=13 }', syms)))
moldyn.statements['s__0_tstep_0_i_13'].add_access_relation(AccessRelation(
        name='a38',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation38 ] : accessRelation38 = i }', syms)))


######
#Line 292: fz(i)  = 0.0;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_0_i_14',
        text='fz( %(a39)s ) = 0.0',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=14 }', syms)))
moldyn.statements['s__0_tstep_0_i_14'].add_access_relation(AccessRelation(
        name='a39',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation39 ] : accessRelation39 = i }', syms)))


######
#Line 299: cutoffSquare = cutoffRadius*cutoffRadius ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_1',
        text='cutoffSquare = cutoffRadius * cutoffRadius',
        iter_space=Set('{ [tstep] : 0 <= tstep && tstep < n_tstep }', syms),
        scatter=Relation('{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=1 && t0=0 && c2=0 }', syms)))


######
#Line 300: n_inter = ninter;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_2',
        text='n_inter = ninter',
        iter_space=Set('{ [tstep] : 0 <= tstep && tstep < n_tstep }', syms),
        scatter=Relation('{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=2 && t0=0 && c2=0 }', syms)))


######
#Line 301: vir  = 0.0 ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_3',
        text='vir = 0.0',
        iter_space=Set('{ [tstep] : 0 <= tstep && tstep < n_tstep }', syms),
        scatter=Relation('{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=3 && t0=0 && c2=0 }', syms)))


######
#Line 302: epot = 0.0;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_4',
        text='epot = 0.0',
        iter_space=Set('{ [tstep] : 0 <= tstep && tstep < n_tstep }', syms),
        scatter=Relation('{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=4 && t0=0 && c2=0 }', syms)))


######
#Line 309: xx = x(inter1(ii)) - x(inter2(ii));
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_0',
        text='xx = x( %(a40)s ) - x( %(a41)s )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=0 }', syms)))
moldyn.statements['s__0_tstep_5_ii_0'].add_access_relation(AccessRelation(
        name='a40',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation40 ] : accessRelation40 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_5_ii_0'].add_access_relation(AccessRelation(
        name='a41',
        data_array=moldyn.data_arrays['x'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation41 ] : accessRelation41 = inter2( ii ) }', syms)))


######
#Line 310: yy = y(inter1(ii)) - y(inter2(ii));
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_1',
        text='yy = y( %(a42)s ) - y( %(a43)s )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=1 }', syms)))
moldyn.statements['s__0_tstep_5_ii_1'].add_access_relation(AccessRelation(
        name='a42',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation42 ] : accessRelation42 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_5_ii_1'].add_access_relation(AccessRelation(
        name='a43',
        data_array=moldyn.data_arrays['y'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation43 ] : accessRelation43 = inter2( ii ) }', syms)))


######
#Line 311: zz = z(inter1(ii)) - z(inter2(ii));
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_2',
        text='zz = z( %(a44)s ) - z( %(a45)s )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=2 }', syms)))
moldyn.statements['s__0_tstep_5_ii_2'].add_access_relation(AccessRelation(
        name='a44',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation44 ] : accessRelation44 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_5_ii_2'].add_access_relation(AccessRelation(
        name='a45',
        data_array=moldyn.data_arrays['z'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation45 ] : accessRelation45 = inter2( ii ) }', syms)))


######
#Line 313: xx += side * (xx < -sideHalf ? 1 : 0); // ^jroelofs if (xx < -sideHalf) xx += side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_3',
        text='xx += side * ( xx < -sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=3 }', syms)))


######
#Line 314: yy += side * (yy < -sideHalf ? 1 : 0); // ^jroelofs if (yy < -sideHalf) yy += side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_4',
        text='yy += side * ( yy < -sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=4 }', syms)))


######
#Line 315: zz += side * (zz < -sideHalf ? 1 : 0); // ^jroelofs if (zz < -sideHalf) zz += side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_5',
        text='zz += side * ( zz < -sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=5 }', syms)))


######
#Line 316: xx -= side * (xx > sideHalf ? 1 : 0);  // ^jroelofs if (xx > sideHalf) xx -= side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_6',
        text='xx -= side * ( xx > sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=6 }', syms)))


######
#Line 317: yy -= side * (yy > sideHalf ? 1 : 0);  // ^jroelofs if (yy > sideHalf) yy -= side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_7',
        text='yy -= side * ( yy > sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=7 }', syms)))


######
#Line 318: zz -= side * (zz > sideHalf ? 1 : 0);  // ^jroelofs if (zz > sideHalf) zz -= side;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_8',
        text='zz -= side * ( zz > sideHalf ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=8 }', syms)))


######
#Line 319: rd = (xx*xx + yy*yy + zz*zz);
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_9',
        text='rd = ( xx * xx + yy * yy + zz * zz )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=9 }', syms)))


######
#Line 323: rd_lt_cutoffSquare = (rd < cutoffSquare ? 1 : 0); // +jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_10',
        text='rd_lt_cutoffSquare = ( rd < cutoffSquare ? 1 : 0 )',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=10 }', syms)))


######
#Line 325: rrd   = 1.0/rd;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_11',
        text='rrd = 1.0 / rd',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=11 }', syms)))


######
#Line 326: rrd2  = rrd*rrd ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_12',
        text='rrd2 = rrd * rrd',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=12 }', syms)))


######
#Line 327: rrd3  = rrd2*rrd ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_13',
        text='rrd3 = rrd2 * rrd',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=13 }', syms)))


######
#Line 328: rrd4  = rrd2*rrd2 ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_14',
        text='rrd4 = rrd2 * rrd2',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=14 }', syms)))


######
#Line 329: rrd6  = rrd2*rrd4;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_15',
        text='rrd6 = rrd2 * rrd4',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=15 }', syms)))


######
#Line 330: rrd7  = rrd6*rrd ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_16',
        text='rrd7 = rrd6 * rrd',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=16 }', syms)))


######
#Line 331: r148  = rrd7 - 0.5 * rrd4 ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_17',
        text='r148 = rrd7 - 0.5 * rrd4',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=17 }', syms)))


######
#Line 333: forcex = xx*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_18',
        text='forcex = xx * r148 * rd_lt_cutoffSquare',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=18 }', syms)))


######
#Line 334: forcey = yy*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_19',
        text='forcey = yy * r148 * rd_lt_cutoffSquare',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=19 }', syms)))


######
#Line 335: forcez = zz*r148 * rd_lt_cutoffSquare; // ^jroelofs;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_20',
        text='forcez = zz * r148 * rd_lt_cutoffSquare',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=20 }', syms)))


######
#Line 337: fx(inter1(ii))  += forcex ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_21',
        text='fx( %(a46)s ) += forcex',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=21 }', syms)))
moldyn.statements['s__0_tstep_5_ii_21'].add_access_relation(AccessRelation(
        name='a46',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation46 ] : accessRelation46 = inter1( ii ) }', syms)))


######
#Line 338: fy(inter1(ii))  += forcey ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_22',
        text='fy( %(a47)s ) += forcey',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=22 }', syms)))
moldyn.statements['s__0_tstep_5_ii_22'].add_access_relation(AccessRelation(
        name='a47',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation47 ] : accessRelation47 = inter1( ii ) }', syms)))


######
#Line 339: fz(inter1(ii))  += forcez ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_23',
        text='fz( %(a48)s ) += forcez',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=23 }', syms)))
moldyn.statements['s__0_tstep_5_ii_23'].add_access_relation(AccessRelation(
        name='a48',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation48 ] : accessRelation48 = inter1( ii ) }', syms)))


######
#Line 341: fx(inter2(ii))  -= forcex ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_24',
        text='fx( %(a49)s ) -= forcex',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=24 }', syms)))
moldyn.statements['s__0_tstep_5_ii_24'].add_access_relation(AccessRelation(
        name='a49',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation49 ] : accessRelation49 = inter2( ii ) }', syms)))


######
#Line 342: fy(inter2(ii))  -= forcey ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_25',
        text='fy( %(a50)s ) -= forcey',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=25 }', syms)))
moldyn.statements['s__0_tstep_5_ii_25'].add_access_relation(AccessRelation(
        name='a50',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation50 ] : accessRelation50 = inter2( ii ) }', syms)))


######
#Line 343: fz(inter2(ii))  -= forcez ;
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_26',
        text='fz( %(a51)s ) -= forcez',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=26 }', syms)))
moldyn.statements['s__0_tstep_5_ii_26'].add_access_relation(AccessRelation(
        name='a51',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, ii ]->[ accessRelation51 ] : accessRelation51 = inter2( ii ) }', syms)))


######
#Line 345: vir  -= rd*r148 * rd_lt_cutoffSquare; // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_27',
        text='vir -= rd * r148 * rd_lt_cutoffSquare',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=27 }', syms)))


######
#Line 346: epot += (rrd6 - rrd3) * rd_lt_cutoffSquare; // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_5_ii_28',
        text='epot += ( rrd6 - rrd3 ) * rd_lt_cutoffSquare',
        iter_space=Set('{ [ tstep, ii ] : 0 <= tstep && tstep < n_tstep && 0 <= ii && ii < n_inter }', syms),
        scatter=Relation('{ [ tstep, ii ]->[ c0, tstep, c1, ii, c2 ] : c0=0 && c1=5 && c2=28 }', syms)))


######
#Line 352: fx(inter1(ii)) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_0',
        text='fx( %(a52)s ) *= timeStepSqHalf',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=0 }', syms)))
moldyn.statements['s__0_tstep_6_i_0'].add_access_relation(AccessRelation(
        name='a52',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation52 ] : accessRelation52 = inter1( ii ) }', syms)))


######
#Line 353: fy(inter1(ii)) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_1',
        text='fy( %(a53)s ) *= timeStepSqHalf',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=1 }', syms)))
moldyn.statements['s__0_tstep_6_i_1'].add_access_relation(AccessRelation(
        name='a53',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation53 ] : accessRelation53 = inter1( ii ) }', syms)))


######
#Line 354: fz(inter1(ii)) *= timeStepSqHalf ; // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_2',
        text='fz( %(a54)s ) *= timeStepSqHalf',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=2 }', syms)))
moldyn.statements['s__0_tstep_6_i_2'].add_access_relation(AccessRelation(
        name='a54',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation54 ] : accessRelation54 = inter1( ii ) }', syms)))


######
#Line 355: vhx(inter1(ii)) += fx(inter1(ii)); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_3',
        text='vhx( %(a55)s ) += fx( %(a56)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=3 }', syms)))
moldyn.statements['s__0_tstep_6_i_3'].add_access_relation(AccessRelation(
        name='a55',
        data_array=moldyn.data_arrays['vhx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation55 ] : accessRelation55 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_6_i_3'].add_access_relation(AccessRelation(
        name='a56',
        data_array=moldyn.data_arrays['fx'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation56 ] : accessRelation56 = inter1( ii ) }', syms)))


######
#Line 356: vhy(inter1(ii)) += fy(inter1(ii)); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_4',
        text='vhy( %(a57)s ) += fy( %(a58)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=4 }', syms)))
moldyn.statements['s__0_tstep_6_i_4'].add_access_relation(AccessRelation(
        name='a57',
        data_array=moldyn.data_arrays['vhy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation57 ] : accessRelation57 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_6_i_4'].add_access_relation(AccessRelation(
        name='a58',
        data_array=moldyn.data_arrays['fy'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation58 ] : accessRelation58 = inter1( ii ) }', syms)))


######
#Line 357: vhz(inter1(ii)) += fz(inter1(ii)); // ^jroelofs
######
moldyn.add_statement(Statement(
        name='s__0_tstep_6_i_5',
        text='vhz( %(a59)s ) += fz( %(a60)s )',
        iter_space=Set('{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }', syms),
        scatter=Relation('{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=6 && c2=5 }', syms)))
moldyn.statements['s__0_tstep_6_i_5'].add_access_relation(AccessRelation(
        name='a59',
        data_array=moldyn.data_arrays['vhz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation59 ] : accessRelation59 = inter1( ii ) }', syms)))
moldyn.statements['s__0_tstep_6_i_5'].add_access_relation(AccessRelation(
        name='a60',
        data_array=moldyn.data_arrays['fz'],
        iter_to_data=Relation('{ [ tstep, i ]->[ accessRelation60 ] : accessRelation60 = inter1( ii ) }', syms)))

print moldyn.codegen('iegen_moldyn_ouput.c')
