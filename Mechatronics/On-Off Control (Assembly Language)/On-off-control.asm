	LIST P = 16F747
	title "Case Study 3"

#include <P16F747.INC>

	__CONFIG _CONFIG1, _FOSC_HS & _CP_OFF & _DEBUG_OFF & _VBOR_2_0 & _BOREN_0 & _MCLR_ON & _PWRTE_ON & _WDT_OFF
	
	__CONFIG _CONFIG2, _BORSEN_0 & _IESO_OFF &_FCMEN_OFF



; PORT Assignments:
; Port B : pin 0-2 is for mode indicators , pin 3 is fault indicator
; Port C : pin 7 is green pin 6 is red
; Port D : pin 7 is main, pin 6 is reduced
; Port E : pin 0-2 is for octal switch


Count   equ 20h ; Counter
Temp    equ 21h ; temporary register
State   equ 22h ; Program state register, stores octal 
Delay   equ 23h ; delay for switch
ADValue equ 24h ; value read from AD
Timer2  equ 25h
Timer1  equ 26h
Timer0  equ 27h
OneSec	equ	28h

;Initial Part
    org 00h
    goto    initPort
    org 04h
    goto    isrService
    org 10h

;   PORT INITIALIZATION  
initPort
    clrf    PORTB ; clear ALL THE PORTS
    clrf    PORTC
    clrf    PORTD
    clrf    PORTE
    bsf     STATUS,RP0  ; set bit in STATUS register for bank 1
    clrf    TRISB       ; configure Port B outputs
    movlw   B'11111111' ; 
    movwf   TRISC       ; configure Port C pins as inputs
    movlw   B'00000111' ; 
    movwf   TRISE       ; configure Port E pin 0,1,2 as octal switch inputs
    movlw   B'00001010' ; Lower four bits 0101 to make octal work
    movwf   ADCON1      ; move to ADCON1 A/D register
    movlw   B'00111111' ; move 0x02 into W 
    movwf   TRISD       ; Port D pin 1 input, others output
    bcf     STATUS,RP0  ; select register bank 0
    clrf    Count       ; zero the count
    clrf    State
    clrf	ADValue


;MAIN CODE SECTION

waitPress
	btfsc   PORTC,7     ; check green button pressed 
	goto    GreenPress  ; when triggered , go to routine
	goto    waitPress   ; if not ,  continue checking

GreenPress
	btfss   PORTC,7     ; check green button still pressed
	goto    waitPress   ; noise ,button not pressed,continue checking

GreenRelease
	btfsc   PORTC,7     ; check green button is released
	goto    GreenRelease; if not, continue waiting
	call    SwitchDelay ; let switch debounce

ModeSelection
	comf    PORTE,0     ; complement PORTE 
	andlw	B'00000111' ; only leave the lower 3 bits of PORTE
	movwf   State       ; move the mode to State register
	movwf   PORTB       ; send the right mode num to LED indicator
	bcf     PORTB,3     ; no initial error 
	bcf     STATUS,Z
	movlw   B'00000001' ; move 0x01 to w register
	xorwf   State,0     ; compare with w to check it is mode 1
	btfsc   STATUS,Z    ; if it is mode 1 
	goto    Mode1     ; goto Mode1
	bcf     STATUS,Z
	movlw   B'00000010' ; move 0x02 to w register
	xorwf   State,0     ; compare with w to check it is mode 2
	btfsc   STATUS,Z    ; if it is mode 2
	goto    Mode2     ; goto Mode2
	bcf     STATUS,Z
	movlw   B'00000011' ; move 0x03 (mode 3) to w register
	xorwf   State,0     ; compare with w to check it is mode 3
	btfsc   STATUS,Z    ; if it is mode 3
	goto    Mode3   ; goto Mode3
	bcf     STATUS,Z
	movlw   B'00000100' ; move 0xF4 to w register
	xorwf   State,0     ; compare with w to check it is mode 4
	btfsc   STATUS,Z    ; if it is mode 4
	goto    Mode4    ; goto Mode4

FaultInit
	clrf    PORTD       ; clear the armature

Loop
	bsf     PORTB,3     ; PortB pin3 LED on
	call    FaultBlinkDelay  ; Port B flash on  
	bcf     PORTB,3     ; PortB pin3 LED off
	call    FaultBlinkDelay  ; port B flash off
	goto    Loop        ; Keep the loop

FaultBlinkDelay
	movlw   06h         ; get most significant hex value +1
	movwf   Timer2      
	movlw   16h
	movwf   Timer1
	movlw   15h
	movwf   Timer0

FaultBlinkDelayLoop
	decfsz  Timer0, F
	goto    FaultBlinkDelayLoop
	decfsz  Timer1, F
	goto    FaultBlinkDelayLoop
	decfsz  Timer2, F
	goto    FaultBlinkDelayLoop
	return

Mode1
	btfsc   PORTC,7     ; check green button pressed;           
	goto    GreenPress
	btfsc   PORTC,6     ; check red button pressed
	goto    RedPress    ; go to redpress
	goto    Mode1     ; continue checking

RedPress
	btfss   PORTC,6     ; check red button still pressed
	goto    Mode1     ; continue checking

RedRelease
	btfsc   PORTC,6     ; check red released
	goto    RedRelease  ; continue checking
	call    SwitchDelay ; debounce
	btfss   PORTC,0     ; check if solenoid sensor tripped
	call    EngageSolenoid   ; if not tripped, then engage solenoid
	btfsc	PORTC,0		; check if solenoid sensor tripped
	call    DisengageSolenoid   ; if it is on, turn off
	goto    Mode1    ; return to Mode1, loop

EngageSolenoid
	bsf     PORTD,7     ; make it engage
	btfsc   PORTC,0     ; check if it is engaged  as an input
	goto    ReducedSolenoid  ; if it is, turn on and off the correct 
	btfss	PORTB,3		; for the LED	; 
	goto	EngageSolenoid	; , wait for it to engage
	goto 	Mode1

ReducedSolenoid
	bsf     PORTD,6     ; turn on the reduced transistor
	bcf     PORTD,7     ; turn off the main transistor
	return

DisengageSolenoid
	bcf     PORTD,7     ; make it disengage
	bcf     PORTD,6     ; turn off the reduced transistor
	btfss   PORTC,0     ; check if it is disengaged
	goto	Mode1		        ; if it is , return
	goto    DisengageSolenoid   ; if not , continue looping

Mode2
	btfsc   PORTC,7     ;check green button pressed
	goto    GreenPress  ; when triggered , go to GreenPress
	btfsc   PORTC,6     ; check red button pressed
	goto    RedPress2    ; go to redpress
	goto    Mode2     ; continue checking

RedPress2
	btfss   PORTC,6     ; check red button still pressed
	goto    Mode2     ; continue checking

RedRelease2
	btfsc   PORTC,6     ; check red released
	goto    RedRelease2  ; continue checking
	call    SwitchDelay ; debounce
	btfss   PORTC,0     ; check if solenoid sensor tripped
	call    EngageSolenoid2   ; if not tripped, then engage solenoid
	bsf 	STATUS,RP0 		; select register bank 1
	movlw 	B'00000100' 	; RA0, RA1, RA3 are analog inputs, the rest digital. 
	movwf 	ADCON1		; move to special function A/D register
	bcf 	STATUS, RP0 	; select register bank 0
	movlw 	B'01000001' 	; select 8 * oscillator, analog input 0, turn on
	movwf 	ADCON0 		; move to special function A/D register
	goto waitLoop
	goto Mode2


waitLoop
	btfsc ADCON0,GO		; check if A/D is finished
	goto waitLoop 		; loop until A/D is finished
	btfsc	ADCON0,GO	; make sure A/D is finished
	goto waitLoop 		; A/D/ not finished, still wait
	movf ADRESH,W		; get A/D value
	movwf ADValue			; display on LEDs
	movf ADRESH,W		; get A/D value
	movwf PORTB			; save thing as ADValue 
	bsf ADCON0, GO		; restart A/D conversion 
	goto LoopStart		; Originally on waitLoop

LoopStart
	movlw   01h         ; get most significant hex value +1
	movwf   Timer2      ; 
	movlw   16h         ;
	movwf   Timer1
	movlw   15h
	movwf   Timer0

LoopDelay
	decfsz  Timer0,F
	goto    LoopDelay
	decfsz  Timer1,F
	goto	LoopDelay
	decfsz  Timer2,F
	goto    LoopDelay
	movf 	ADValue,W		; get A/D value
	movwf 	PORTB			; save thing as ADValue CONFIRMED, THIS WORKS. 
	decfsz	ADValue,F
	goto	LoopStart
	btfsc	PORTC,0		; check if solenoid sensor tripped
	goto    DisengageSolenoid2   ; if it is on, turn off

EngageSolenoid2
	bsf     PORTD,7     ; make it engage
	btfsc   PORTC,0     ; check if it is engaged  as an input
	goto    ReducedSolenoid2  ; if it is, turn on and off the correct 
	btfss	PORTB,3		; for the LED	; 
	goto	EngageSolenoid2	; , wait for it to engage
	goto 	Mode2

ReducedSolenoid2
	bsf     PORTD,6     ; turn on the reduced transistor
	bcf     PORTD,7     ; turn off the main transistor
	return

DisengageSolenoid2
	bcf     PORTD,7     ; make it disengage
	bcf     PORTD,6     ; turn off the reduced transistor
	btfss   PORTC,0     ; check if it is disengaged
	goto    DisengageSolenoid2   ; if not , continue looping
	goto	ModeSelection		        ; if it is , return

Mode3
	btfsc   PORTC,7     ;check green button pressed
	goto    GreenPress  ; when triggered , go to GreenPress
	clrf	PORTD     ; init of PORTD, pin 4
	movlw   B'01000001' ; select 8 * oscillator , analog input 0 , turn on
	movwf   ADCON1      ; move to special function A/D register
	call    ADDelay     ; delay for Tad prior to A/D start
	bsf     ADCON0,GO   ; start A/D conversion
	call    ADwaitLoop  ; 
	btfsc   PORTC,6     ; check red button pressed
	goto    RedPress3   ; go to red press mode 3
	goto    Mode3

RedPress3
	btfsc   PORTC,6     ; check red button released
	goto    RedPress3   ; noise , continue checking

RedRelease3
	btfsc	PORTC,6		; wait until release
	goto	RedRelease3 ; wait until release
	btfsc   PORTD,4     ; if PORTD , pin 4 is 0, turn it on,
	goto    Mode3   ; else goto Mode3
	goto	waitLoop3     ; goto WaitLoop3

waitLoop3
	btfsc ADCON0,GO		; check if A/D is finished
	goto waitLoop3 		; loop until A/D is finished
	btfsc	ADCON0,GO	; make sure A/D is finished
	goto waitLoop3 		; A/D/ not finished, still wait
	movf ADRESH,W		; get A/D value
	movwf ADValue			;
	movf ADRESH,W		; get A/D value
	movwf PORTB			; save thing as ADValue CONFIRMED, THIS WORKS. 
	bsf ADCON0, GO		; restart A/D conversion WE DO NOT WANT IT TO RESTART. 
	movlw B'00000000'; 
	subwf ADValue,W; 
	btfss	STATUS,C	; 
	call	FaultInit	
	bcf     STATUS,Z
	movlw   B'00000000' ; move 0xF4 (mode 4) to w register
	xorwf   ADValue,0     ; compare with w to check it is mode 4
	btfsc   STATUS,Z    ; if it is mode 4 (Z will be 1)
	goto    FaultInit    ; goto Mode4
	movlw	B'01110000' ; set W as 70h
	subwf	ADValue,1	; substract W from ADvalue, save result in W
	btfss	STATUS,C	; 
	call	DisengageSolenoid3	; if ADValue < 70h, disengage
	btfsc	STATUS,C	; check the borrow register in Status
	call	EngageSolenoid3	; if ADValue > 70h, engage
	goto waitLoop3	

EngageSolenoid3
	bsf     PORTD,7     ; make it engage
	btfsc   PORTC,0     ; check if it is engaged  as an input
	goto    ReducedSolenoid3  ; if it is, turn on and off the correct 
	btfss	PORTB,3		; for the LED	; 
	goto	EngageSolenoid3	; , wait for it to engage
	goto 	waitLoop3 

ReducedSolenoid3
	bsf     PORTD,6     ; turn on the reduced transistor
	bcf     PORTD,7     ; turn off the main transistor
	return

DisengageSolenoid3
	bcf     PORTD,7     ; make it disengage
	bcf     PORTD,6     ; turn off the reduced transistor
	btfss   PORTC,0     ; check if it is disengaged
	goto    DisengageSolenoid3   ; if not , continue looping
	goto	waitLoop3 	        ; if it is , return

Mode4
	btfsc   PORTC,7     ;check green button pressed
	goto    GreenPress  ; when triggered ,  	
	btfsc   PORTC,6     ; check red button pressed
	goto    RedPress4    ; go to redpress
	goto    Mode4     ; continue checking

RedPress4
	btfss   PORTC,6     ; check red button still pressed
	goto    Mode4     ; continue checking

RedRelease4
	btfsc   PORTC,6     ; check red released
	goto    RedRelease4  ; continue checking
	call    SwitchDelay ; debounce
	btfss   PORTC,0     ; check if solenoid sensor tripped
	call    EngageSolenoid4   ; if not tripped, then engage solenoid
	bsf     PORTD,6     ; turn on the reduced transistor
	bcf     PORTD,7     ; turn off the main transistor
	bsf 	STATUS,RP0 		; select register bank 1
	movlw 	B'00000100' 	; RA0, RA1, RA3 are analog inputs, the rest digital. 
	movwf 	ADCON1		; move to special function A/D register
	bcf 	STATUS, RP0 	; select register bank 0
	movlw 	B'01000001' 	; select 8 * oscillator, analog input 0, turn on
	movwf 	ADCON0 		; move to special function A/D register
	goto waitLoop
	goto Mode4

waitLoop4
	btfsc ADCON0,GO		; check if A/D is finished
	goto waitLoop4 		; loop until A/D is finished
	btfsc	ADCON0,GO	; make sure A/D is finished
	goto waitLoop		; A/D/ not finished, still wait
	movf ADRESH,W		; get A/D value
	movwf ADValue		; display on LEDs
	movf ADRESH,W		; get A/D value
	movwf PORTB			; save thing as ADValue CONFIRMED, THIS WORKS. 
	bsf ADCON0, GO		; restart A/D conversion WE DO NOT WANT IT TO RESTART. 
	goto LoopStart4		; Originally on waitLoop

LoopStart4
	movlw   01h         ; get most significant hex value +1
	movwf   Timer2      ; 
	movlw   16h         ;
	movwf   Timer1
	movlw   15h
	movwf   Timer0

LoopDelay4

	decfsz  Timer0,F
	goto    LoopDelay4
	decfsz  Timer1,F
	goto	LoopDelay4
	decfsz  Timer2,F
	goto    LoopDelay4
	movf 	ADValue,W		; get A/D value
	movwf 	PORTB			; save thing as ADValue CONFIRMED, THIS WORKS. 
	decfsz	ADValue,F
	goto	LoopStart4
	btfsc	PORTC,0		; check if solenoid sensor tripped
	goto    DisengageSolenoid4   ; if it is on, turn off

EngageSolenoid4
	bsf     PORTD,7     ; make it engage
	btfsc   PORTC,0     ; check if it is engaged  as an input
	goto    ReducedSolenoid4  ; if it is, turn on and off the correct 
	btfss	PORTB,3		; for the LED	; 
	goto 	LoopStart4

ReducedSolenoid4

	bsf     PORTD,6     ; turn on the reduced transistor
	bcf     PORTD,7     ; turn off the main transistor
	return

DisengageSolenoid4
	bcf     PORTD,7     ; make it disengage
	bcf     PORTD,6     ; turn off the reduced transistor
	btfss   PORTC,0     ; check if it is disengaged
	goto    DisengageSolenoid4   ; if not , continue looping
	goto	ModeSelection		        ; if it is , return

ADwaitLoop
	btfsc   ADCON1,GO   ; check if A/D is finished
	goto    ADwaitLoop  
	return

SwitchDelay
	movlw   D'20'
	movwf   Delay
	goto    DebDelay

ADDelay
	movlw   03h
	movwf   Delay
	goto    DebDelay

DebDelay
	decfsz  Delay, F
	goto    DebDelay
	return

isrService
	goto	isrService

	END
