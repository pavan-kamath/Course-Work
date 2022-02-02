#include <xc.h>
#include <pic.h>
#include <stdio.h>

    #pragma config  FOSC=HS, CP=OFF, DEBUG=OFF, BORV=20, BOREN=0, MCLRE=ON, PWRTE=ON, WDTE=OFF
    #pragma config  BORSEN=OFF, IESO=OFF, FCMEN=0
/* Note: the format for the CONFIG directive starts with a double underscore.
The above directive sets the oscillator to an external high speed clock, 
sets the watchdog timer off, sets the power up timer on, sets the system
clear on (which enables the reset pin) and turns code protect off. */
/**************************************************************
Timer.c
This is a translation of Timer.asm into C.
This program illustrates using a long integer (32 bits) to form a timer
with a one second period. 
Since a "for" delay loop is 26 usec using an unsigned long number
(determined in the simulator), you need approximately 38,461 loops to
equal 1 second. It therefore requires at least 2 8-bit registers to store
this large a number. An unsigned long is 4 registers. (Note: if you use an
unsigned integer to hold the value, the for loop is quicker and the value
needed does not fit into the 2 registers.)
  Hardware for this program is the Mechatronics microcomputer board.
  The program counts the seconds and displays the count as an 8 bit
  binary value on Port D. The LEDs on Port D should therefore increment
by one every second.
**************************************************************/
// Variable declarations 

#define PORTBIT(adr,bit)    ((unsigned)(&adr)*8+(bit))
    // The function PORTBIT is used to give a name to a bit on a port
    // The variable RC0 could have equally been used
        static bit greenButton @ PORTBIT(PORTC,1);
        static bit redButton @ PORTBIT(PORTC,0);
        static bit R_Uni_Sensor @ PORTBIT(PORTA,0);
        static bit B_Uni_Sensor @ PORTBIT(PORTA,1);
        static bit L_Bi_Sensor @ PORTBIT(PORTA,2);
        static bit B_Bi_Sensor @ PORTBIT(PORTA,3);
        static bit E0 @ PORTBIT(PORTE,0);
        static bit E1 @ PORTBIT(PORTE,1);
        static bit E2 @ PORTBIT(PORTE,2);

        static bit D0 @ PORTBIT(PORTD, 0);

        
        char i;
        int MODE, Count, redpressed, greenpressed; //using separate variables redpressed and greenpressed to know the status of the button press for easier understanding since PORTBIT readings are flipped
        unsigned long Timer; // Holds value for 1 sec timer
        
        
    void init(void)
    {
  
//        PCFG3 = 1; 
//        PCFG2 = 1; 
//        PCFG1 = 1;
//        PCFG0 = 0; 
        RBIE = 0; 
        INT0IE = 0; 


        PORTA = 0B00000000; // cClear Port A
        TRISA = 0B11111111; // configure Port A as all input

        
        ADCON1 = 0B00001111;
        PORTB = 0B00000000; // cClear Port B
        TRISB = 0B00000000; // configure Port B as all output
        PORTC = 0B00000000; // cClear Port C
        TRISC = 0B11111111; // configure Port C as all input

        //PORTE = 0b00000000; // cClear Port E
        TRISE = 0B00001111; // configure Port E as all input
        TRISD = 0B00000000; // configure Port D as all output
        PORTD = 0B00000000; // Clear Port A
        

        //char Mode; 

    
    }

    
void SwitchDelay (void) // Waits for switch debounce
{
    for (Timer=300; Timer > 0; Timer--) {} // 200 μs delay
}
    

void LongDelay (void) // custom delay
{
    for (Timer=200; Timer > 0; Timer--) {} // 1200 μs delay
}
    
void OneSecDelay (void) // custom delay
{
    for (Timer=38461; Timer > 0; Timer--) {} // 1 sec delay
}

void UniFullCW (void) //define full step CW motion for UniPolar Motor
{

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 1;

    LongDelay();

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay();      

}

void UniFullCCW (void) //define full step CCW motion for UniPolar Motor
{

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay(); 

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 1;

    LongDelay();
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

       
}

void UniWaveCW (void) //define wave drive CW motion for UniPolar Motor
{

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay();      

}

void UniWaveCCW (void) //define wave drive CCW motion for UniPolar Motor
{

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay(); 

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

       
}

void UniHalfCW (void) //define half step CW motion for UniPolar Motor
{

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();   
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 1;

    LongDelay();

    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay();

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay(); 
    

}

void UniHalfCCW (void) //define half step CCW motion for UniPolar Motor
{

    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay(); 
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 1;

    LongDelay();
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 1;

    LongDelay();
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 1;
    PORTDbits.RD3 = 0;

    LongDelay();   
    
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();
    
    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 1;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();
    
    PORTDbits.RD0 = 1;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;

    LongDelay();
 
}

void BiCW (void) //define full step CW motion for BiPolar Motor
{
        
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay(); 
    
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 1;

    LongDelay(); 
    
    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 0;

    LongDelay();
    
    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay();





   

}

void BiCCW (void) //define full step CCW motion for BiPolar Motor
{
    
    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay();

    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 0;

    LongDelay();

    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 1;

    LongDelay();

    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay();      

}

void BiWaveCCW (void) //define wave drive CW motion for BiPolar Motor
{
        
    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 1;

    LongDelay(); 
    
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 1;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 0;

    LongDelay(); 
    
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 1;

    LongDelay();
    
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 1;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay();
 

}

void BiWaveCW (void) //define wave drive CCW motion for BiPolar Motor
{
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 1;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 0;

    LongDelay();
    
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 1;

    LongDelay();
        
    PORTDbits.RD4 = 0;
    PORTDbits.RD5 = 1;
    PORTDbits.RD6 = 1;
    PORTDbits.RD7 = 0;

    LongDelay(); 
    
    PORTDbits.RD4 = 1;
    PORTDbits.RD5 = 0;
    PORTDbits.RD6 = 0;
    PORTDbits.RD7 = 1;

    LongDelay(); 


}




void ModeDef (void) //check for position of Mode knob on the board
{
MODE = 50; //AN IMPOSSIBLE MODE
    
    while(MODE == 50) // infinite loop
    {
        
        while (greenButton == 0 && MODE == 50)// && E0 == 1 && E1 == 1 && E2 == 1)   //(greenButton == 0)
        {

            SwitchDelay(); // A timer which adds a little delay. 

            
            if (E0 == 1 && E1 == 1 && E2 == 1) //checking mode input based on mode knob on the board
            {
                MODE = 0; //set MODE variable to selected mode number
                PORTB = PORTE; //display mode number using PortB LEDs for visual confirmation
            }
            
            if (E0 == 0 && E1 == 1 && E2 == 1)   //(greenButton == 0)
            {
                MODE = 1;
                PORTB = PORTE;
            } 
            
            if (E0 == 1 && E1 == 0 && E2 == 1)   //(greenButton == 0)
            {
                MODE = 2;
                PORTB = PORTE;
            } 
            
            if (E0 == 0 && E1 == 0 && E2 == 1)   //(greenButton == 0)
            {
                MODE = 3;
                PORTB = PORTE;
            } 
            
            if (E0 == 1 && E1 == 1 && E2 == 0)   //(greenButton == 0)
            {
                MODE = 4;
                PORTB = PORTE;
            } 
        }             
    }        
    
    
    
}

void ModeOne (void) //define MODE 1
{
    while(R_Uni_Sensor==1 && redpressed == 0 && greenButton == 1) //set both motors to home position
        {
            UniFullCCW();
        }

        while(L_Bi_Sensor==1 && redpressed == 0 && greenButton == 1)
        {
            BiCCW();
        }

        while (redButton == 1 && redpressed == 0 && greenButton == 1) //wait for red button press
        {
            redpressed = 0;
        }

        redpressed = 1; 

        while(B_Uni_Sensor==1 && redpressed == 1 && greenButton == 1 && MODE==1) //rotate unipolar motor to the bottom sensor by the shortest distance
        {
            UniFullCW();
        }
		
        redpressed = 0;

         while (redButton == 1 && redpressed == 0 && greenButton == 1 && MODE==1)  //wait for red button press
        {
            redpressed = 0;
        }
		
        redpressed = 1;
        
		if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef(); //check for position of mode knob and change the mode
        }

        while(B_Bi_Sensor==1 && redpressed == 1 && greenButton == 1 && MODE==1) //rotate bipolar motor to the bottom sensor by the shortest distance
        {
            BiCCW();
        }
        
		redpressed = 0;

        while (redButton == 1 && redpressed == 0 && greenButton == 1 && MODE==1)  //wait for red button press
        {
            redpressed = 0;
        }
        
		redpressed = 1;
        
		if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef(); //check for position of mode knob and change the mode
        }

        while(R_Uni_Sensor==1 && redpressed == 1 && greenButton == 1 && MODE==1) //rotate unipolar motor to the right/home sensor by the shortest distance
        {
            UniFullCCW();
        }

        redpressed = 0;
		
        while (redButton == 1 && redpressed == 0 && greenButton == 1 && MODE==1)  //wait for red button press
        {
            redpressed = 0;
        }
        
		redpressed = 1;
        
		if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef(); //check for position of mode knob and change the mode
        }

        while(L_Bi_Sensor==1 && redpressed == 1 && greenButton == 1 && MODE==1) //rotate bipolar motor to the left/home sensor by the shortest distance
        {
            BiCW();
        }
        
		redpressed = 0;

        while (redButton == 1 && redpressed == 0 && greenButton == 1 && MODE==1)  //wait for red button press
        {
            redpressed = 0;
        }

        redpressed = 1;
        
        if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef(); //check for position of mode knob and change the mode
        }
}

void ModeTwo (void)  //define MODE 2
{	//set home position
    while(R_Uni_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        UniFullCCW();
    }

    while(L_Bi_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        BiCCW();
    }

    while (redButton == 1 && redpressed == 0 && greenButton == 1)
    {
        redpressed = 0;
    }

    redpressed = 1;

    while((B_Uni_Sensor==1 || B_Bi_Sensor==1) && greenButton==1) //rotate both motors simultaneously in opposite directions, full-stepping
    {
        if (B_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniFullCW();
        }
        //redpressed = 0;

        if (B_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiCCW();
        }
    }
    
    
    while((R_Uni_Sensor==1 || L_Bi_Sensor==1) && greenButton==1 ) //rotate both motors simultaneously in opposite directions, full-stepping
    {
        
        
        if (R_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniFullCCW();
        }
        //redpressed = 0;

        if (L_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiCW();
        }
    }
        
    while (redButton == 0) //check if red button is pressed and held
    {
        redpressed = 0; 
        
        if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef();
        }
        
    }
    SwitchDelay();  

    while (redpressed == 0 && redButton == 1)// if red button as pressed, wait for next step
    {
        if (redButton == 0)
        {
            redpressed = 1; //restart if red button is pressed again
        }
        
        if (greenButton == 0)
        {    
            ModeDef(); //check mode knob position and change mode
            
            redpressed = 1; 
        }
    }
              
}    

void ModeThree (void)  //define MODE 3
{	//rotate to home position, bottom sensor for unipolar and left sensor for bipolar motor
    while(B_Uni_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        UniFullCCW();
    }

    while(L_Bi_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        BiCCW();
    }

    while (redButton == 1 && redpressed == 0 && greenButton == 1)
    {
        redpressed = 0;
    }

    redpressed = 1;

    while((R_Uni_Sensor==1 || B_Bi_Sensor==1) && greenButton==1 ) //rotate both motors simultaneously in same directions, full-stepping
    {
        
        
        if (R_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniFullCW();
        }
        //redpressed = 0;

        if (B_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiCW();
        }
    }
	
    while((B_Uni_Sensor==1 || L_Bi_Sensor==1) && greenButton==1) //rotate both motors back to the starting positions simultaneously in same directions, full-stepping
    {
        if (B_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniFullCCW();
        }
        //redpressed = 0;

        if (L_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiCCW();
        }
    }
    
    
    
        
    while (redButton == 0) //check if red button is pressed and held
    {
        redpressed = 0; 
        
        if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef();
        }
        
    }
    SwitchDelay();  

    while (redpressed == 0 && redButton == 1)// if red button as pressed, wait for next step
    {
        if (redButton == 0)
        {
            redpressed = 1; //restart if red button is pressed again
        }
        
        if (greenButton == 0)
        {    
            ModeDef();
            
            redpressed = 1;  //check mode knob position and change mode
        }
    }
             
}    

void ModeFour (void)  //define MODE 4
{	//set unipolar motor to right sensor and bi polar to left sensor
    while(R_Uni_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        UniWaveCCW();
    }

    while(L_Bi_Sensor==1 && redpressed == 0 && greenButton == 1)
    {
        BiWaveCCW();
    }

    while (redButton == 1 && redpressed == 0 && greenButton == 1)
    {
        redpressed = 0;
    }

    redpressed = 1;

    while((B_Uni_Sensor==1 || B_Bi_Sensor==1) && greenButton==1) //rotate both motors simultaneously in opposite directions, wave drive motion
    {
        if (B_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniWaveCW();
        }
        //redpressed = 0;

        if (B_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiWaveCCW();
        }
    }
    
    
    while((R_Uni_Sensor==1 || L_Bi_Sensor==1) && greenButton==1 ) //rotate both motors simultaneously back to starting position in opposite directions, wave drive motion
    {
        
        
        if (R_Uni_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            UniWaveCCW();
        }
        //redpressed = 0;

        if (L_Bi_Sensor==1 && redpressed == 1 && greenButton == 1)
        {
            BiWaveCW();
        }
    }
        
    while (redButton == 0)//check if red button is pressed and held
    {
        redpressed = 0; 
        
        if (greenButton == 0) //check if green button is pressed
        {    
            ModeDef();
        }
        
    }
    SwitchDelay();  

    while (redpressed == 0 && redButton == 1)// if red button as pressed, wait for next step
    {
        if (redButton == 0)
        {
            redpressed = 1; //restart if red button is pressed again
        }
        
        if (greenButton == 0)
        {    
            ModeDef();
            
            redpressed = 1;  //check mode knob position and change mode
        }
    }
              
}

void main(void)
{
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    // Initialization of port D & Counter
    
    init();
    SwitchDelay();
    PORTDbits.RD0 = 0;
    PORTDbits.RD1 = 0;
    PORTDbits.RD2 = 0;
    PORTDbits.RD3 = 0;
    Count = 0; // clear counter
    //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
    ModeDef(); 
    
    while (greenButton == 0) // To ensure it doesn't jump to next thing
    {
    
    }
    
    redpressed = 0;
    greenpressed = 0; 
    LongDelay(); 
    
    ModeDef(); 
    
    while (1 != 2)
    {
        while (MODE == 1 && greenButton == 1)
        {
            ModeOne();
        }
        while (MODE == 2 && greenButton == 1)
        {
            ModeTwo();
        }
        while (MODE == 3 && greenButton == 1)
        {
            ModeThree();
        }
        while (MODE == 4 && greenButton == 1)
        {
            ModeFour();
        }
    }
    
}    
    
