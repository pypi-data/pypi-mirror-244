************************************************************************
* ******************************************************************** *
* *                                                                  * *
* *   MM      MM     AA     TTTTTTTT  HH    HH             QQQQQQ    * *
* *   MMM    MMM    A  A       TT     HH    HH            QQ    QQ   * *
* *   MM M  M MM   A    A      TT     HH    HH            QQ    QQ   * *
* *   MM  MM  MM  AAAAAAAA     TT     HHHHHHHH            QQ    QQ   * *
* *   MM      MM  AA    AA     TT     HH    HH            QQ    QQ   * *
* *   MM      MM  AA    AA     TT     HH    HH            QQ   QQQ   * *
* *   MM      MM  AA    AA     TT     HH    HH  =========  QQQQQQ    * *
* *                                                             QQ   * *
* *         General mathematical procedures: QUADRATURES             * *
* *                                                                  * *
* ******************************************************************** *
*                                                                      *
*  ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,  *
*  ,                                                                ,  *
*  ,     Vadim Naumov, INFN, Sezione di Firenze and LTP, ISU        ,  *
*  ,                                                                ,  *
*  , Version of August 15, 1997  for MS 32-bit FORTRAN PowerStation ,  *
*  ,                                                                ,  *
*  ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,  *
*                                                                      *
* ******************************************************************** *
* *                                                                  * *
* *                                                                  * *
* *    GGGGGG             MM      MM    -------------------------    * *
* *   GG    GG            MMM    MMM   |                         |   * *
* *   GG         eeeeee   MM M  M MM   | ADAPTIVE QUADRATURE FOR |   * *
* *   GG        ee    ee  MM  MM  MM   |   ONE-FOLD  INTEGRALS   |   * *
* *   GG   GGG  eeeeeeee  MM      MM   | by Genz-Malik algorithm |   * *
* *   GG    GG  ee        MM      MM   |                         |   * *
* *    GGGGGG     eeeee   MM      MM    -------------------------    * *
* *                                                                  * *
* *                                                                  * *
* *   ------------------------------------------------------------   * *
* *   E N T R I E S:                                                 * *
* *   GeMSet(FunG,res,Xlow,Xupp,RelErr,MinCal,*)                     * *
* *   GeMInt(FunG,res,Xlow,Xupp,*)                                   * *
* *   GeMInf                                                         * *
* *   ------------------------------------------------------------   * *
* *                                                                  * *
* ******************************************************************** *
************************************************************************
      SUBROUTINE GeMSet(FunG,res,Xlow,Xupp,RelErr,MinCal,*)
************************************************************************

         IMPLICIT REAL (A-H,O-Z)

         SAVE EPS,MinPTS,MaxPTS,MinFin,MaxFin

         LOGICAL(2) Flag

*     THE FOLLOWING TWO PARAMETERS MUST BE SPECIFIED BEFORE USING !

         INTEGER, PARAMETER ::
     ,            Nlog  = 10,                                            LogFile number (open in MAIN)
     ,            Length= 1000000,                                       Length > 6
     ,            MinMax= 17*(2.0d+00*Length/7-1),
     ,            Lim2  = Length-7
            REAL, PARAMETER ::
     ,            Zero  =    0.0d+00,
     ,            One   =    1.0d+00,
     ,            Half  =    1.0d+00/2,
     ,            V1    = -971.0d+00/729,
     ,            V2    =  245.0d+00/486,
     ,            V3    =   65.0d+00/1458,
     ,            V4    =   25.0d+00/729,
     ,            W1    = -424.0d+00/2187,
     ,            W2    =  980.0d+00/6561,
     ,            W3    =  340.0d+00/6561,
     ,            W4    =  200.0d+00/19683,
     ,            W5    = 6859.0d+00/78732,
c    ,            Y2    =    0.3585685828003181,                         3/SQRT(70)
c    ,            Y4    =    0.9486832980505138,                         3/SQRT(10)
c    ,            Y5    =    0.6882472016116853                          3/SQRT(19)
     ,            Y2    =    0.358568582800318091990645153907938d+00,    3/SQRT(70)
     ,            Y4    =    0.948683298050513799599668063329816d+00,    3/SQRT(10)
     ,            Y5    =    0.688247201611685297721628734293623d+00     3/SQRT(19)

         ALLOCATABLE STORE(:)                                            storage array

         EPS=RelErr
         MinPTS=MinCal
         MaxPTS=MinMax+MinPTS
         MinFin=MaxPTS
         MaxFin=MinPTS

         RETURN

*     ================================================================ *
      ENTRY GeMInt(FunG,Res,Xlow,Xupp,*)
*     ================================================================ *
        Flag=.FALSE.
      NFcall=0
       NsubR=7
       LsubR=7
      Output=Zero
      AbsErr=Zero
         CTR=(Xupp+Xlow)*Half
         WTH= Xupp-CTR
         Vir=Half
      ALLOCATE(STORE(Length))
    1 VolRGN=4*WTH*Vir
        Sum1=FunG(CTR)
           V=WTH*Y2
        Sum2=FunG(CTR-V)+FunG(CTR+V)
           V=WTH*Y4
        Sum4=FunG(CTR-V)+FunG(CTR+V)
         IF (7*Sum2.EQ.Sum4+12*Sum1) THEN
           Ndiv=2
                                     ELSE
           Ndiv=1
      endIF
         V=2*Sum1
      Sum2=V+Sum2
      Sum3=V+Sum4
      Sum4=2*Sum4
         IF (WTH.EQ.Zero) THEN
           NFcall=NFcall+5
           IF (Vir.GT.Zero) THEN
             Sum5=Sum1
                            ELSE
             Sum5=V
        endIF
           GOTO 2
      endIF
         V=WTH*Y5
         IF (WTH.GT.Zero) THEN
           NFcall=NFcall+7
           IF (Vir.GT.Zero) THEN
             Sum5=2*(FunG(CTR-V)+FunG(CTR+V))
                           ELSE
             Sum5=   FunG(CTR-V)+FunG(CTR+V)
        endIF
                         ELSE
             IF (Vir.GT.Zero) THEN
               NFcall=NFcall+7
               Sum5=2* FunG(CTR-V)+FunG(CTR+V)
                              ELSE
               NFcall=NFcall+6
               Sum5=   FunG(CTR-V)
          endIF
      endIF
    2 ErrRGN=VolRGN*(V1*Sum1+V2*Sum2+V3*Sum3+V4*Sum4)
      ValRGN=VolRGN*(W1*Sum1+W2*Sum2+W3*Sum3+W4*Sum4+W5*Sum5)
      ErrRGN=ABS(ErrRGN-ValRGN)
      Output=    Output+ValRGN
      AbsErr=    AbsErr+ErrRGN
         IF (Flag) THEN
    3      IsubR=2*NsubR
           IF (IsubR.GT.LsubR) GOTO 5
           IF (IsubR.LT.LsubR) THEN
             I=IsubR+7
             IF (STORE(IsubR).LT.STORE(I)) IsubR=I
        endIF
           IF (ErrRGN.GE.STORE(IsubR)) GOTO 5
           DO k=0,6
             STORE(NsubR-k)=STORE(IsubR-k)
        endDO
           NsubR=IsubR
           GOTO 3
      endIF
    4 IsubR=(NsubR/14)*7
         IF (IsubR.GE.7.AND.ErrRGN.GT.STORE(IsubR)) THEN
           DO k=0,6
             STORE(NsubR-k)=STORE(IsubR-k)
        endDO
           NsubR=IsubR
           GOTO 4
      endIF
    5 IsubR=NsubR-6
      STORE(IsubR  )=Vir
      STORE(NsubR-4)=WTH
      STORE(NsubR-3)=CTR
      STORE(NsubR-2)=Ndiv
      STORE(NsubR-1)=ValRGN
      STORE(NsubR  )=ErrRGN
         IF (Flag) THEN
           Flag=.FALSE.
           IF (Nd.EQ.1) CTR=CTR+2*WTH
           LsubR=LsubR+7
           NsubR=LsubR
           GOTO 1
      endIF
         IF (AbsErr.LE.EPS*ABS(Output).AND.NFcall.GE.MinPTS) THEN
           DEALLOCATE (STORE)
           MinFin=MIN(MinFin,NFcall)
           MaxFin=MAX(MaxFin,NFcall)
           res=Output                                                    Tutto va bene
           RETURN
      endIF
         IF (NFcall.GT.MaxPTS) THEN
           WRITE(*   ,101) MaxPTS,Eps                                    Error message (screen)
           WRITE(Nlog,101) MaxPTS,Eps                                    Error message (LogFile)
           GOTO 6
      endIF
         IF (LsubR.GT.Lim2) THEN
           WRITE(*   ,102) Length,Eps                                    Error message (screen)
           WRITE(Nlog,102) Length,Eps                                    Error message (LogFile)
           GOTO 6
      endIF
        Flag=.TRUE.
       NsubR=7
       IsubR=1
         Vir=       STORE(1)
         WTH=       STORE(3)
         CTR=       STORE(4)
          Nd=       STORE(5)
      Output=Output-STORE(6)
      AbsErr=AbsErr-STORE(7)
         IF (Nd.EQ.1) THEN
           WTH=Half*WTH
           CTR= CTR-WTH
                     ELSE
           Vir=Half*Vir
      endIF
      GOTO 1
    6 CONTINUE
      DEALLOCATE (STORE)
         IF (Output.NE.Zero) THEN
           WRITE(Nlog,201) AbsErr/ABS(Output),NFcall
                             ELSE
           WRITE(Nlog,202) AbsErr,NFcall
      endIF
      RETURN 1

*     ================================================================ *
      ENTRY GeMInf
*     ================================================================ *
      WRITE (*   ,300) EPS,MaxPTS,MinPTS,Length,MaxFin,MinFin
      WRITE (Nlog,300) EPS,MaxPTS,MinPTS,Length,MaxFin,MinFin
      MinFin=MaxPTS
      MaxFin=MinPTS
      RETURN

  101 FORMAT(/ '  GEM: THE MAXIMUM NUMBER OF INTEGRAND CALLS,',I15,
     ,         ', IS TOO SMALL'/'  FOR THE REQUIRED ACCURACY:',1pd8.1)
  102 FORMAT(/ '  GEM: THE STORAGE ARRAY LENGTH,',I10,
     ,         ', IS TOO SMALL'/'  FOR THE REQUIRED ACCURACY:',1pd8.1)
  201 FORMAT(              '  RELATIVE ERROR =',1pd9.2,
     ,                       ', NUMBER OF INTEGRAND CALLS =',I13/)
  202 FORMAT(  '  RESULT = 0! ABSOLUTE ERROR =',1pd9.2,
     ,                       ', NUMBER OF INTEGRAND CALLS =',I13/)
  300 FORMAT(/33x,'GEMINFORM'/
     /         3x,69('-')/'  | RelErr =',1PD10.3,' | MaxCal =',I15,
     ,                     ' | MinCal =',    I12,' |'/
     /                    '  | Length =',    I10,' | MaxFin =',I15,
     ,                     ' | MinFin =',    I12,' |'/3x,69('-')/)
      END SUBROUTINE GeMSet