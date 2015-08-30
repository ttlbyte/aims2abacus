#!/usr/bin/python
#to do: convert the constrain information of atoms.
import sys,os
if os.path.exists('geometry.in'):
    pass;
else:
    print("geometry.in not exits")
    exit(-1);
i=0;
j=0;
k=0;
l=0;
vectorlist=[]
atomtype=[]
atom_coor=[]
atom_coor_full=[]
a2b=1.88972666
with open('geometry.in','r') as fin:
    line=fin.readline();
    while(len(line)>0):
        while(line[0]==' '):
            line=line[1:]
        if len(line)<=1:
            line=fin.readline();
            continue;
        if line[0]=='#':      #ingore white spaces at the begining of lines
            pass;
        if line.split()[0]=='lattice_vector':
            vectorlist.append([line.split()[1],line.split()[2],line.split()[3]])
            i+=1;              #store the vector information
        if line.split()[0]=='constrain_relaxation':
            constrain=line.split()[1];
            if constrain=='.true.':
                atom_coor[-1][3]='0';
                atom_coor[-1][4]='0';
                atom_coor[-1][5]='0';
            if constrain=='x':
                atom_coor[-1][3]='0';
            if constrain=='y':
                atom_coor[-1][4]='0';
            if constrain=='z':
                atom_coor[-1][5]='0';
            else:
                pass;
        if line.split()[0]=='atom_frac':
            atomname=line.split()[4];
            if atomname not in atomtype:
                if (len(atom_coor)>0):
                    atom_coor_full.append(atom_coor);
                    atom_coor=[];
                atomtype.append(atomname);
                j+=1;
            atom_coor.append([line.split()[1],line.split()[2],line.split()[3],'1','1','1']);
            l+=1;
        if line.split()[0]=='atom':
            k=1;
            atomname=line.split()[4];
            if atomname not in atomtype:
                if (len(atom_coor)>0):
                    atom_coor_full.append(atom_coor);
                    atom_coor=[];
                atomtype.append(atomname);
                j+=1;
            atom_coor.append([line.split()[1],line.split()[2],line.split()[3],'1','1','1']);
        line=fin.readline();
atom_coor_full.append(atom_coor);
#store the coordinates of atoms
l=0;
with open('STRU','w') as fout:
    fout.write('LATTICE_CONSTANT\n');
    fout.write('1   //add lattice constant(a.u.)\n')
    while (i>=1):
        fout.write(str("%0.8f" % (float(vectorlist[l][0])*a2b))+' '+str("%0.8f" % (float(vectorlist[l][1])*a2b))+' '+str("%0.8f" % (float(vectorlist[l][2])*a2b))+'\n');
        l+=1;
        i-=1;
    fout.write('\n');
    fout.write('ATOMIC_POSITIONS\n');
    if k==0:
        fout.write('Direct   //Direct or Cartesian coordinate\n');
    else:
        fout.write('Cartesian    //Direct or Cartesian coordinate\n');
    fout.write('\n');
    m=len(atomtype)-1;
    while(m>=0):
        fout.write('\n');
        fout.write(atomtype[m]+'\n');
        fout.write("0.000   //starting magnetism\n");
        i=len(atom_coor_full[m]);
        fout.write(str(i)+'    //number of atoms\n');
        i-=1;
        while(i>=0):
            fout.write(atom_coor_full[m][i][0]+' '+atom_coor_full[m][i][1]+' '+atom_coor_full[m][i][2]+' '+atom_coor_full[m][i][3]+' '+atom_coor_full[m][i][4]+' '+atom_coor_full[m][i][5]+'\n')
            i-=1;
        m-=1;
