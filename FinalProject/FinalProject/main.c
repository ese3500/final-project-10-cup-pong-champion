/*
 * main.c
 *
 * Created: 4/30/2024 8:07:39 PM
 *  Author: jdmarsh
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)
#include <stdlib.h>
#include <stdio.h>
#include <util/delay.h>
#include <util/delay.h>
#define gravity 9.81
double height;
double launchVelocity;

int spiInterrupt= 0;
char StringX[50];
char StringY[50];

float x;
float y;

//double cupHeight;


int main(void)
{
    /* Replace with your application code */
	cli();
 	Initialize_Timer_1();
	Initialize_Timer_2();
 	initPWM();
	sei();
// 	Set_Servo_2(90); // Initialize theta value(where 90 degrees is facing forwards)
 	Set_Servo_1(90); 
	//Set_Servo_0(90);
	Set_DC_Duty_Cycle(10);
	_delay_ms(3000);
	Set_DC_Duty_Cycle(50);
    while (1) 
    {

    }
}



void initPWM(){
	//Speaker Output Timer!!
	//Set PB2 as an output
	DDRB |= (1<<DDB2);
	PORTB &= ~(1<<PORTB2);
	//Set Timer0 to be FastPWM, Timer2 = 16MHz
	TCCR0A |= (1<<WGM00);
	TCCR0A |= (1<<WGM02);
	TCCR0B &= ~(1<<WGM01);
	//Timer0 prescaled to 64
	TCCR0B |= (1<<CS00);
	TCCR0B |= (1<<CS01);
	TCCR0B &= ~(1<<CS02);
	//Enable output compare
	TIMSK0|= (1<<OCIE0A);
	
	//Clear flags
	TIFR0 |= (1<<OCF0A);
	
	OCR0A = 100;
}

ISR(TIMER0_COMPA_vect){
	PORTB ^= (1<<PORTB2);
}
void Set_DC_Duty_Cycle(int percent){
	OCR0A = (int)((255*percent)/100);
}

void Initialize_Timer_1() {
	

	
	// Set OC1A (PB1) as output pin
	DDRB |= (1 << DDB1);
	
	// Prescaler of 256
	TCCR1B &= ~(1 << CS12);
	TCCR1B |= (1 << CS11);
	TCCR1B |= (1 << CS10);
	
	// Set Timer1 in Fast PWM mode
	TCCR1A |= (1 << WGM10);
	TCCR1A |= (1 << WGM11);
	TCCR1B |= (1 << WGM12);
	TCCR1B |= (1 << WGM13);
	
	// Clear OC1A on compare match, set OC1A at BOTTOM
	TCCR1A &= ~(1 << COM1A1);
	TCCR1A |= (1 << COM1A0);
	
	TIMSK1 |= (1 << OCIE1A);
	
	OCR1A = 250;
	

}
ISR(TIMER1_COMPA_vect) {
	// Toggle PD6 output
	PORTB ^= (1 << PORTB1);
}

void Get_Servo_Deg(float x, float y){
	
	int deg = (int)(atan(y/x)*180/3.14);
	return deg;
	}
void Set_Servo_1(int deg){
	int degAdj = deg + 120;
	int a = OCR1A;
	int b=(int)(1.44*degAdj+49);
	OCR1A = b;
// 	for (int a =1; a==100;a++){
// 		OCR1A += (x-y)/100;
// 		_delay_ms(2);
// 	}
}

void Initialize_Timer_2() {
	
	
	
	// Set OC2A (PB3) as output pin
	DDRB |= (1 << DDB3);
	
	TCCR2B |= (1 << CS22);
	TCCR2B |= (1 << CS20);
	TCCR2B &= ~(1 << CS21);
		
	TCCR2A |= (1 << WGM20);
	TCCR2A |= (1 << WGM21);
	TCCR2B |= (1 << WGM22); // WGM[2:0] = 0x5 , TOP = OCR0A
		


	TCCR2A &= ~(1 << COM2A1);
	TCCR2A |= (1 << COM2A0);
		
	TIMSK2 |= (1 << OCIE2A);
		
	OCR2A = 85;
	
}
ISR(TIMER2_COMPA_vect) {
	// Toggle PB3 output
	PORTB ^= (1 << PORTB3);
}
void Set_Servo_2(double deg){
	OCR2A=(int)(1.3888*deg+49);
}



void SPI_SlaveInit(void)

{
	PRR1 &= ~(1 << PRSPI1);

	/* Set MISO output, all others input */

	DDRC |= (1<<DDC0);

	/* Enable SPI */

	SPCR1 |= (1<< SPIE1);
	SPCR1 |= (1<< SPE1);
	
	// LSB First
	
	SPCR1 |= (1<<DORD1);
	
	SPCR1 &= ~(1<<MSTR1);
	SPCR1 &= ~(1<<CPOL1);
	SPCR1 &= ~(1<<CPHA1);
}
ISR(SPI1_STC_vect) {
	// Set interrupt flag
	spiInterrupt += 1;
	
	if (spiInterrupt == 1){
		x = SPDR1;
		} else{
		y = SPDR1;
	}
	
}