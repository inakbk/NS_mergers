      program interface_traj
      implicit double precision (a-h,o-z)
      parameter (npart=21000)
      dimension ipart(npart),ampart(npart),rhomaxpart(npart),
     &  tempmaxpart(npart),yepart(npart),anglepart(npart),
     &  tau1part(npart),tau2part(npart),tmaxpart(npart)
      character*100 cmd
      character*30 cdate
      character*20 filein,filejob,fileaa,host
      logical lexist
c iplateform=1 --> IAA   computers
c iplateform=2 --> HYDRA computers
c iplateform=3 --> Lemaitre2 computers
      isys=system('hostname > hostfile ')
      open(unit=10,file='hostfile')
      read(10,'(a)') host
      close(10)
      iplateform=2
      if (host(1:5).eq.'astro') iplateform=1
      if (host(1:2).eq.'lm') iplateform=3

      open(unit=10,file='traj.in')
      read(10,*) inode
      read(10,*) itrajstep
      read(10,*)
      i=1 
      amtot=0.
  100 read(10,*,end=110,err=110) ii,am,ro,te,ye12,ye0,texp,tt
      ipart(i)=ii
      ampart(i)=am
      rhomaxpart(i)=ro
      tempmaxpart(i)=te
      yepart(i)=ye0
      anglepart(i)=0.
      tmaxpart(i)=tt
      tau1part(i)=-99.
      tau2part(i)=-99.
      amtot=amtot+ampart(i)
      i=i+1
      goto 100
  110 close(10)
      ipmax=i-1
c
      inquire(file='node.in',exist=lexist)
      if (lexist) then
        open(unit=10,file='node.in')
        read(10,*) inode
        close(10)
      endif
c
      if (iplateform.ne.1) isys=system('rm jobrunning.dat')
      cmd='cp txxx.in Abon'
      isys=system(cmd)
      cmd='cp traj.in Abon'
      isys=system(cmd)
c
c skip cases that have been already treated
      isys=system('grep "  A   Solar  "
     &    Abon/aa??????? > overandout')
      ipid=0
      iloop=0
      do ip=1,ipmax,itrajstep
    
c skip cases that have been already treated
        open(unit=10,file='overandout')
   99   read(10,'(7x,i7,16x,1p,e9.2)',end=98) ipdone,tfin
        if (ipdone.eq.ipart(ip).and.tfin.gt.1.d2) then
          close(10)
          cycle
        endif
        goto 99
   98   close(10)

c check if given trajectory already calculated
        if (iplateform.ge.1) then
          write(fileaa,'("noh",i7.7)') ipart(ip) 
c       elseif (iplateform.ge.2) then
c         write(fileaa,'("Abon/pf_aa",i7.7)') ipart(ip) 
        endif
        inquire(file=fileaa,exist=lexist)
        if (lexist) cycle

c read number of jobs running
        do while (.true.)
          isys=system( 'sleep 5' )
          njob=inode
          iloop=iloop+1
          if (iloop.ge.999999) iloop=0
          call runningjobs(njob,iplateform,iloop)
          if (njob.lt.inode) exit 
        enddo

c run individual trajectory

c prepare input file 
c   define name of the trajectory input file
        write(filein,'("t",i7.7,".in")') ipart(ip) 
c   prepare initial abundance file: only values of 0.10;0.15;0.20;...;0.50;0.55
        iye3=idnint(yepart(ip)*200)
        iye3=iye3*5
        if (iye3.gt.55) iye3=55
        if (iye3.lt.10) iye3=10
        write(cmd,1000) ipart(ip),iye3,ipart(ip),filein
 1000   format('sed "s/xxxxxxx/',i7.7,'/g; s/yyy/',i3.3,
     &    '/g; s/zzzz/',i4.4,'/g" txxx.in >',a20)
        isys=system(cmd)
c prepare & run job
        if (iplateform.eq.1) then
          write(cmd,'("/home/sgoriely/Astro/Eos/Rpro/rpro19.x < t",
     &      i7.7,".in >noh",i7.7," &")') ipart(ip),ipart(ip)
        elseif (iplateform.eq.2) then
          write(filejob,'("rpro",i7.7,".job")') ipart(ip) 
          write(cmd,1002) ipart(ip),filejob
 1002     format('sed "s/xxxxxxx/',i7.7,'/g" rproxxx.job > ',a20)
          isys=system(cmd)
          write(cmd,'("qsub -m n ",a20)') filejob
        elseif (iplateform.eq.3) then
          write(filejob,'("rpro",i7.7,".sh")') ipart(ip) 
          write(cmd,1003) ipart(ip),filejob
 1003     format('sed "s/xxxxxxx/',i7.7,'/g" rproxxx.sh  > ',a20)
          isys=system(cmd)
          write(cmd,'("sbatch ",a20)') filejob
        endif
        isys=system(cmd)
        isys=system('date >  pidlast')
        if (iplateform.eq.1) 
     &    isys=system('ps x O -T | grep rpro | grep -v grep >> pidlast')
        open(unit=11,file='pidlast')
        read(11,'(a30)') cdate
        if (iplateform.eq.1) read(11,*) ipid
        close(11)
        isys=system( 'sleep 1' )
        open(unit=11,file='jobrunning.dat',position='append')
        write(11,'(i4," : job for trajectory = ",i7,
     &    " running with PID=",i7," on ",a20," since ",a30)')
     &    ip,ipart(ip),ipid,trim(host),cdate
        close(11) 
      enddo
      isys=system('rm pidlast hostfile')
      end

      subroutine runningjobs(njob,iplateform,iloop)
      implicit double precision (a-h,o-z)
      character*100 cmd,filetoto
      i=0
      write(filetoto,'("toto",i6.6)') iloop
      if (iplateform.eq.1) then
        cmd='ps x | grep rpro | grep -v grep >'//trim(filetoto)
        isys=system(cmd)
      elseif (iplateform.eq.2)  then
        cmd='qstat | grep " R " >'//trim(filetoto)
        isys=system(cmd)
        cmd='qstat | grep " Q " >>'//trim(filetoto)
        isys=system(cmd)
      elseif (iplateform.eq.3)  then
        cmd='squeue -l -j -u sgoriely | grep " RUNN ">'//trim(filetoto)
        isys=system(cmd)
        cmd='squeue -l -j -u sgoriely | grep " PEND ">>'//trim(filetoto)
        isys=system(cmd)
      endif
      open(unit=10,file=trim(filetoto),status='old',err=30)
   10 read(10,*,end=20,err=20)
      i=i+1
      goto 10
   20 close(10)
      cmd='rm '//trim(filetoto)
      isys=system(cmd)
      if (iplateform.eq.1) then
        njob=i
      else
        njob=i
      endif
   30 return
      end
