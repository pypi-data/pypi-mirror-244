************************************************************************
* ******************************************************************** *
* *                                                                  * *
* *   MM      MM     AA     TTTTTTTT  HH    HH             SSSSSS    * *
* *   MMM    MMM    A  A       TT     HH    HH            SS    SS   * *
* *   MM M  M MM   A    A      TT     HH    HH            SS         * *
* *   MM  MM  MM  AAAAAAAA     TT     HHHHHHHH              SSSS     * *
* *   MM      MM  AA    AA     TT     HH    HH                  SS   * *
* *   MM      MM  AA    AA     TT     HH    HH            SS    SS   * *
* *   MM      MM  AA    AA     TT     HH    HH  =========  SSSSS     * *
* *                                                                  * *
* *       General mathematical procedures: SPLINE FUNCTIONS          * *
* *                                                                  * *
* *       =======  TWO-DIMENSIONAL SPLINE FUNCTIONS  ======          * *
* *                                                                  * *
* ******************************************************************** *
*  ##################################################################  *
*  #                                                                #  *
*  #     Vadim Naumov, INFN, Sezione di Firenze and LTP, ISU        #  *
*  #                                                                #  *
*  #  Version of Dec. 28, 1997  for MS 32-bit FORTRAN PowerStation  #  *
*  #                                                                #  *
*  ##################################################################  *
************************************************************************
      SUBROUTINE Coeff2(Mode,Issue,NX,NY,Xmin,Ymin,Xmax,Ymax,F,C,Quiz,L)
************************************************************************
*                                                                      *
*   This routine is almost perfect analogue of  'Coeff1' at  Mult = 0  *
*   and Tie = F but it is designed for interpolating the functions of  *
*   two variables defined in rectangular regions.                      *
*                                                                      *
*   C is the ONE-DIMENSIONAL array of spline coefficients; the number  *
*   of its elements must be no less than (NX+2)*(NY+2).                *
*                                                                      *
*   L plays two different parts:                                       *
*                                                                      *
* * when L = 0, the routine doesn't calculate the spline coefficients  *
*   C, but does install all the parameters for the function 'Inter2';  *
*                                                                      *
* * when L > 0, the L defines the start point for checking up the in-  *
*   terpolation accuracy in the reference points [L < MIN(NX,NY)].     *
*                                                                      *
************************************************************************

         IMPLICIT REAL*8 (A-H,O-Z)
               LOGICAL(2) Quiz
         REAL*8 Inter2
         REAL*8,PARAMETER:: Zero=0, One=1, Three=3, r=One/256

         PARAMETER (NXmax=  10000)                                       User's setting (NYmax > 2)
         PARAMETER (NYmax=  10000)                                       User's setting (NYmax > 2)
         PARAMETER (Nlog =     10)                                       Open UNIT=Nlog in called program
         PARAMETER (Const=1.0d-50)

         DIMENSION C(*),F(NX,NY)                                         NX .LE. NXmax, NY .LE. NYmax
         ALLOCATABLE G(:,:)                                              storage array

*        ------------------------------------------------------------- *
*        ATTENTION !   If it is impossible to use ALLOCATABLE  dimen-  *
*                      sion G(:), comment lines 58, 89, 131  and  un-  *
*                      comment lines 64, 65, 66, 67.                   *
*                                                                      *
*        DIMENSION G(NXmax+4,NYmax+4) ! storage array
*        INCLUDE 'E:/FORTRAN/Sources/Shared/Include/Heap.fi'             Naumov
*        INCLUDE 'G:/FORTRAN/Sources/Shared/Include/Heap.fi'             Kuzmin
*        EQUIVALENCE (G(1,1),Heap(1)) ! memory saving
*        ------------------------------------------------------------- *
         Transf(Func)=SQRT(Func)                                         Example of using the Mode=4 regime
*        ------------------------------------------------------------- *
*        Installation of parameters in the function 'Inter2':
*        ------------------------------------------------------------- *
         IF (Mode.LT.1.OR.Mode.GT.3) THEN
           STOP ' Improper value for the interpolation mode in Coeff2 '
      endIF

         SX=(Xmax-Xmin)/(NX-1)                                           Interpolation step over variable X
         SY=(Ymax-Ymin)/(NY-1)                                           Interpolation step over variable Y

         discrM=
     #   Inter2(Issue,C,Xmax,Ymax,Mode,NX,NY,Xmin,Ymin,SX,SY,F(1,1))

         IF (L.EQ.0) RETURN                                              When spline coefficients are known
*        ------------------------------------------------------------- *
*        Calculation of the spline coefficients:
*        ------------------------------------------------------------- *
         ALLOCATE(G(NXmax+4,NYmax+4))
         DO 1 n=1,NY
         n2=n+2
         DO 1 m=1,NX
         m2=m+2
         IF (Mode.EQ.1) G(m2,n2) =           F(m,n) *r
         IF (Mode.EQ.2) G(m2,n2) =       LOG(F(m,n))*r
         IF (Mode.EQ.3) G(m2,n2) = LOG(Const+F(m,n))*r
         IF (Mode.EQ.4) G(m2,n2) =    Transf(F(m,n))*r
    1 endDO
         m1=NX+1
         n1=NY+1
*        m2=m1+1
*        n2=n1+1
         m3=m2+1
         n3=n2+1
         m4=m3+1
         n4=n3+1
         DO m=3,m2
           G(m, 2)=Three*(G(m, 3)-G(m, 4))+G(m, 5)                       1
           G(m, 1)=Three*(G(m, 2)-G(m, 3))+G(m, 4)                       2
           G(m,n3)=Three*(G(m,n2)-G(m,n1))+G(m,NY)                       3
           G(m,n4)=Three*(G(m,n3)-G(m,n2))+G(m,n1)                       4
      endDO
         DO n=1,n4
           G( 2,n)=Three*(G( 3,n)-G( 4,n))+G( 5,n)                       1
           G( 1,n)=Three*(G( 2,n)-G( 3,n))+G( 4,n)                       2
           G(m3,n)=Three*(G(m2,n)-G(m1,n))+G(NX,n)                       3
           G(m4,n)=Three*(G(m3,n)-G(m2,n))+G(m1,n)                       4
      endDO
         DO 2 n=1,n2
         n3=n+1
         n4=n+2
         k=(n-1)*m2
         DO 2 m=1,m2
         m3=m+1
         m4=m+2
         C(k+m) = G(m4,n)+G(m,n4)+G(m4,n4)+G(m3,n3) *100
     -          -(G(m3,n)+G(m,n3)+G(m4,n3)+G(m3,n4))*10+G(m,n)
    2 endDO

         DEALLOCATE(G)
*        ------------------------------------------------------------- *
*        Checking up the interpolation accuracy (for entry 'Sp2'):
*        ------------------------------------------------------------- *
         IF (Quiz) THEN
           IF (L.GE.NX.OR.L.GE.NY) STOP ' Failure access to COEFF2 '
           discrA=Zero
           discrQ=Zero
           Null=0
           NXNY=(NX-L+1)*(NY-L+1)
           DO 3 m=L,NX
             X=Xmin+SX*(m-1)
             DO 3 n=L,NY
             IF (F(m,n).NE.Zero) THEN
               Y=Ymin+SY*(n-1)
               Z=One-Sp2(Issue,C,X,Y)/F(m,n)
               Y=ABS(Z)
               IF (Y.GT.discrM) THEN
                 discrM=Y
                 m1=m
                 n1=n
            endIF
               discrA=discrA+Z
               discrQ=discrQ+Y**2
                                 ELSE                                    F(m,n)=0
               Null=Null+1
          endIF
    3   endDO
*           WRITE(Nlog,101) Mode,Issue,NX,NY,NXNY,Null
           IF (Null.LT.NXNY) THEN
             discrA=discrA/(NXNY-Null)
             discrQ=SQRT(discrQ)/(NXNY-Null)
*             WRITE(Nlog,102) discrM,m1,n1,discrA,discrQ
                             ELSE                                        Null=NXNY
*             WRITE(Nlog,103)
        endIF
      endIF
*        ------------------------------------------------------------- *

*  101 FORMAT(/2x,62('_')/' | ',60('-'),' |'/
*     #' | Test of Inter2 [Mode=',I1,', Issue=',I6,']',
*     #' in NX*NY reference points |'/' | ',60('-'),' |'/
*     #' |  NX =',I5,',  NY =',I5,',  Ntot =',I8,',  Null =',I8,5x,'|')
*  102 FORMAT(' |   Maximum Discrepancy =',1pd9.1,'    [node = (',
*     # I4,',',I4,')],',4x,'|'/
*     #' |  Averaged Discrepancy =',1pd9.1,29x,'|'/
*     #' | Quadratic Discrepancy =',1pd9.1,29x,'|'/' |',62('_'),'|'/)
*  103 FORMAT('  | Input function is null in all reference points',13x,
*     #                                         '  |'/'  |',62('_'),'|'/)
      END SUBROUTINE Coeff2

************************************************************************
      FUNCTION Inter2(Issue,C,X,Y,Mode0,NX0,NY0,Xmin0,Ymin0,SX,SY,F11)
************************************************************************
*                                                                      *
*  This is a near-perfect analogue of procedure 'Inter1' at Mult = 0,  *
*  but for functions of two variables defined in rectangular regions.  *
*                                                                      *
*  ------------------------------------------------------------------  *
*  ATTENTION! This version includes an extremely primitive "clamping"  *
*             in the origin (Xmin,Ymin). It is useful in some instan-  *
*             ces but may be removed at will (taking Eps = 0).         *
*  ------------------------------------------------------------------  *
*                                                                      *
************************************************************************

         IMPLICIT REAL*8 (A-H,O-Z)
         REAL*8 C(*), Inter2,Invers

         SAVE NX,NY,Xmin,Xmax,Ymin,Ymax,StepX,StepY
         SAVE Mode,Vertex,Nstop,Delta,A1,A2,A3,B1,B2,B3,M1,M2,M3

         PARAMETER (MaxIss=900000)                                       User's setting (0 < MaxIss < 100)
         PARAMETER (MaxNst=    10**9)                                       User's setting (MaxNst > 0)
         PARAMETER (Nlog  =    10)                                       Open UNIT=Nlog in called program
         PARAMETER (Const = 1.0d-50)
         PARAMETER (Zero=0, One=1, Half=One/2, Quart=One/4, Eps=1.0d-7)

         DIMENSION Xmin(MaxIss),Xmax(MaxIss),StepX(MaxIss),NY(MaxIss)
         DIMENSION Ymin(MaxIss),Ymax(MaxIss),StepY(MaxIss),NX(MaxIss)
         DIMENSION Mode(MaxIss),Delta(MaxIss),Vertex(MaxIss)

         Invers(Func)=Func**2                                            Example of using the Mode=4 regime
         Mode(Issue)=Mode0                                               "Interpolation code"
         NX(Issue)=NX0                                                   Number of interpolation nodes over X
         NY(Issue)=NY0                                                   Number of interpolation nodes over Y
         Xmin(Issue)=Xmin0                                               Left end point on X axis
         Ymin(Issue)=Ymin0                                               Left end point on Y axis
         Xmax(Issue)=X                                                   Right end point on X axis
         Ymax(Issue)=Y                                                   Right end point on Y axis
         StepX(Issue)=SX                                                 Interpolation step over X
         StepY(Issue)=SY                                                 Interpolation step over Y
         Vertex(Issue)=F11                                               = F(1,1)  [see 'Coeff2']
         Inter2=Zero                                                     Initialization of discrM in 'Coeff2'
         Nstop=0                                                         Constant to manage the emergency exit

         Delta(Issue)=Eps*MIN(SX,SY)

************************************************************************
*  When (X,Y) is in the Delta-neighbourhood of the point (Xmin,Ymin),  *
*  the value of the function is taken to be Vertex (if Eps > 0).       *
************************************************************************

         RETURN

*     ================================================================ *
      ENTRY Sp2(Issue,C,X,Y)
*     ================================================================ *
*         PRINT 676,X,Y,Issue,MaxNst
         D =Delta(Issue)
         A1=X-Xmin(Issue)
         A2=Xmax(Issue)-X
         IF (A1.LT.-D.OR.A2.LT.-D) THEN
           Sp2=Vertex(Issue)
*           WRITE(Nlog,101) X,Xmin(Issue)-D,Xmax(Issue)+D
*           WRITE(Nlog,103) D,Issue,NX(Issue),NY(Issue)
           Nstop=Nstop+1
*           IF (Nstop.GT.MaxNst) STOP 'CRASH LANDING FROM Sp2 [X]'
           RETURN
      endIF
         B1=Y-Ymin(Issue)
         B2=Ymax(Issue)-Y
         IF (B1.LT.-D.OR.B2.LT.-D) THEN
           Sp2=Vertex(Issue)
*           WRITE(Nlog,102) Y,Ymin(Issue)-D,Ymax(Issue)+D
*           WRITE(Nlog,103) D,Issue,NX(Issue),NY(Issue)
           Nstop=Nstop+1
*           IF (Nstop.GT.MaxNst) STOP 'CRASH LANDING FROM Sp2 [Y]'
           RETURN
      endIF
         IF (A1.LE.D.AND.B1.LE.D) THEN
           Sp2=Vertex(Issue)
           RETURN
      endIF
         A3=A1/StepX(Issue)
         B3=B1/StepY(Issue)
         M1=IDNINT(A3)                                 ! = INT(A3+Half)
         M2=IDNINT(B3)                                 ! = INT(B3+Half)

! V !    IF (M1*M2.LT.0.OR.M1.ge.NX(Issue)or.M2.ge.NY(Issue)) THEN ! V !
! E !    Sp2=Vertex(Issue)                                         ! E !
! R !    Nstop=Nstop+1                                             ! R !
! S !    WRITE(Nlog,104) X,Y,M1,M2                                 ! S !
! I !    WRITE(Nlog,103) D,Issue,NX(Issue),NY(Issue)               ! I !
! O !    IF (Nstop.GT.MaxNst) STOP 'CRASH LANDING FROM Sp2'        ! O !
! N ! endIF                                                        ! N !

         A3=A3-M1
         B3=B3-M2
         A2=A3**2+Quart
         B2=B3**2+Quart
         A1=A2-A3
         B1=B2-B3
         A3=A2+A3
         B3=B2+B3
         A2=2-(A2+A2)
         B2=2-(B2+B2)
         M3=NX(Issue)+2
         M1=M1+M2*M3+1
         M2=M1+M3
         M3=M2+M3
         D =(A1*C(M1)+A2*C(M1+1)+A3*C(M1+2))*B1
     +     +(A1*C(M2)+A2*C(M2+1)+A3*C(M2+2))*B2
     +     +(A1*C(M3)+A2*C(M3+1)+A3*C(M3+2))*B3
*         PRINT 677,D
         GOTO (1,2,3,4) Mode(Issue)
    1    Sp2=D
         RETURN
    2    Sp2=EXP(D)
         RETURN
    3    Sp2=EXP(D)-Const
         RETURN
    4    Sp2=Invers(D)
         RETURN

*     ================================================================ *
      ENTRY rSp2(Issue,C)             ! May be called only after 'Sp2'
*     ================================================================ *

         D =(A1*C(M1)+A2*C(M1+1)+A3*C(M1+2))*B1
     +     +(A1*C(M2)+A2*C(M2+1)+A3*C(M2+2))*B2
     +     +(A1*C(M3)+A2*C(M3+1)+A3*C(M3+2))*B3
         GOTO (10,20,30,40) Mode(Issue)
   10    rSp2=D
         RETURN
   20    rSp2=EXP(D)
         RETURN
   30    rSp2=EXP(D)-Const
         RETURN
   40    rSp2=Invers(D)
         RETURN

*  101 FORMAT(/'  Mistake! X =',1PD20.13,' lies OUTSIDE the range'/
*     #        '  Xmin-Delta =',1PD20.13,' to Xmax+Delta =',1PD20.13)
*  102 FORMAT(/'  Mistake! Y =',1PD20.13,' lies OUTSIDE the range'/
*     #        '  Ymin-Delta =',1PD20.13,' to Ymax+Delta =',1PD20.13)
*  103 FORMAT( '  Delta =',1PD8.2,
*     #                    '  [Issue =',I6,', NX =',I4,', NY =',I4,']'/)
*  104 FORMAT(/'  Mistake! X=',1PD16.10,', Y=',1PD16.10,
*     #                      ', M1=',I4,', M1=',I4)
*  676 FORMAT('What x and y',E11.5,10x,E11.5,10x,I5,10x,I5)
  677 FORMAT('what is D',E11.5)
      END FUNCTION Inter2
