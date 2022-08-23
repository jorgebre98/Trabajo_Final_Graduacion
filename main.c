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

/*  PROYECT DEFINES */
#define TRANSMIT_BUFFER_SIZE 32

float pwm_value; // Valor recibido para escribir en el PWM.
int32 angle_Quad; // Lectura del decodificador de cuadratura.
bool runcode = false; // Para iniciar/detener el proceso dentro de la interrupción se puede activar/apagar desde el switch principal (case)

CY_ISR_PROTO(isr_Control_Handler);
CY_ISR(isr_Control_Handler){
    if (runcode == 1){
        CyPins_SetPin(LED_EJECUCION_0); // Enciende al iniciar la interrupción (Activo en bajo)
        PWM_1_WriteCompare(pwm_value); // Escribe el valor de pwm.
        angle_Quad = QuadDec_1_GetCounter(); // Obtiene valor del decodificador.
        CyPins_ClearPin(LED_EJECUCION_0);
        }
}
                    
int main(void)
{
    CyGlobalIntEnable; // Enable global interrupts.
    
    float data_receive; // Variable to store UART received character.
    //uint8 EmulatedData = 0; // Variable used to send emulated data.
    
    /* Flags used to store transmit data commands */
    uint8 ContinuouslySendData = 0;
    uint8 SendSingleByte = 0;
    uint8 SendEmulatedData = 0;
    
    float TransmitBuffer[TRANSMIT_BUFFER_SIZE]; // Transmit Buffer.
    
    /*START COMPONENTS*/
    UART_1_Start();
    PWM_1_Start();
    QuadDec_1_Start();
    Timer_1_Start();
    isr_control_StartEx(isr_Control_Handler);
    
    UART_1_PutString("COM Ports Open"); // Verify port connected.

    for(;;)
    {
        /* Place your application code here. */
        data_receive = UART_1_GetChar();
        /*switch(data_receive){
            case (0):
                break;
            case ('c'):
            case ('C'):
                SendSingleByte = 1;
                runcode = true;
                break;
            case ('s'):
            case ('S'):
                ContinuouslySendData = 1;
                break;
            case ('x'):
            case ('X'):
                ContinuouslySendData = 0;
                break;
            case ('e'):
            case ('E'):
                SendEmulatedData = 1;
                break;
            default:
                break;
        }
        
        if (SendSingleByte || ContinuouslySendData){
            sprintf(TransmitBuffer,"Hello World \r\n");
            UART_1_PutString(TransmitBuffer);
            SendSingleByte = 0;
        }
        else if(SendEmulatedData){
            sprintf(TransmitBuffer,"Hello Kim \r\n");
            UART_1_PutString(TransmitBuffer);
            SendEmulatedData = 0;
        }*/
    }
}

/* END OF FILE */
