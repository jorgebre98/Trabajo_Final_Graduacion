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

uint8 pwm_value; // Valor recibido para escribir en el PWM.
int angle_Quad; // Lectura del decodificador de cuadratura.
bool runcode = false; // Para iniciar/detener el proceso dentro de la interrupción se puede activar/apagar desde el switch principal (case)

CY_ISR_PROTO(isr_Control_Handler);
CY_ISR(isr_Control_Handler){
    if (runcode == true){
        CyPins_SetPin(LED_EJECUCION_0); // Enciende al iniciar la interrupción (Activo en bajo)
        PWM_1_WriteCompare(pwm_value); // Escribe el valor de pwm.
        angle_Quad = QuadDec_1_GetCounter(); // Obtiene valor del decodificador.
        CyPins_ClearPin(LED_EJECUCION_0);
    }
}
                    
int main(void)
{
    CyGlobalIntEnable; // Enable global interrupts.
    
    /*START COMPONENTS*/
    UART_1_Start();
    PWM_1_Start();
    QuadDec_1_Start();
    Timer_1_Start();
    isr_control_StartEx(isr_Control_Handler);
    
    UART_1_ClearRxBuffer(); 
    UART_1_ClearTxBuffer();
    
    int32 entero;
    int8 aux;
    uint8* arr = &entero;
    int angle = 0, prev = 0;
    runcode = true;
    
    for (;;){
        pwm_value = UART_1_ReadRxData();
        entero = angle_Quad;
        
        aux = arr[3];
        arr[3] = arr[0];
        arr[0] = aux;
        
        aux = arr[1];
        arr[1] = arr[2];
        arr[2] = aux;
        
        UART_1_PutArray((uint8*)arr,4);
        CyDelay(20);
    }
}