/* ========================================
 *
 * Copyright Jorge Brenes Alfaro, 2022
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * UART COMUNICATION
 *
 * ========================================
*/
#include <project.h>
#include "stdio.h"
#include <stdbool.h>

uint16 pwm_value; // Receive value to write on PWM.
int angle_Quad; // Reading the quadrature decoder.
bool runcode = false; // To start/stop the process into the interrupt. It can be turn on/off in the principal switch(case).

CY_ISR_PROTO(isr_Control_Handler);
CY_ISR(isr_Control_Handler){
    if (runcode == true){
        CyPins_SetPin(LED_EJECUCION_0); // Turns on at interrupt start (Active low)
        PWM_1_WriteCompare(pwm_value); // Write the pwm's value.
        angle_Quad = QuadDec_1_GetCounter(); // Read the decoder's value.
        CyPins_ClearPin(LED_EJECUCION_0); // Turns off at interrupt stop.
    }
}
                    
int main(void)
{
    CyGlobalIntEnable; // Enable global interrupts.
    
    /**** START COMPONENTS ****/
    UART_1_Start();
    PWM_1_Start();
    QuadDec_1_Start();
    Timer_1_Start();
    isr_control_StartEx(isr_Control_Handler);
    
    /**** CLEAR TRANSMIT/RECEIVE BUFFER ****/
    UART_1_ClearRxBuffer(); 
    UART_1_ClearTxBuffer(); 
    
    //**** AUXILIARY VARIABLES ****/
    int32 entero;
    int8 aux; 
    uint8* arr = (uint8*)&entero;
    uint16 lsb,msb;    
    
    
    runcode = true; // Start the interrupts.
    
    for (;;){
        // Receive a 2-byte data for the pwm
        msb = UART_1_ReadRxData(); //Read serial port.
        lsb = UART_1_ReadRxData();
        pwm_value = lsb + (msb << 8);
        
        // Send the angular value
        
        //entero = pwm_value;
        entero = angle_Quad; // Asign the quad_dec value.
        
        /**** REORDER THE BYTES TO TRASNMIT ****/
        aux = arr[3];
        arr[3] = arr[0];
        arr[0] = aux;
        
        aux = arr[1];
        arr[1] = arr[2];
        arr[2] = aux;
        
        UART_1_PutArray((uint8*)arr,4); // Transmitting the quad_dec value.
        CyDelay(20);
    }
}