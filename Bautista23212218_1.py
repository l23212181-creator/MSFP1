"""
Práctica 1: Diseño de un controlador para un sistema de segundo orden

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Jesus Geovanny Bautista Paz
Número de control:23212181
Correo institucional: l23212181@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

"""
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N)
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1
u3 = t/tend
u4 = np.sin(m.pi/2*t)
u = np.column_stack((u1,u2,u3,u4))
signals = ["step","impulse","ramp","sinusoidal"]

# Componentes del circuito RLC
R,L,C = 2.2E3,22E-6,470E-6
num = [L*C*R, R*C*R+L, R]
den = [3*L*C*R, 5*R*C*R+L, 2*R]
sys = ctrl.tf(num,den)
print(f"Función de transferencia: {sys}\n")

# Polos del sistema
L = np.roots(den)
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")

# Componentes del controlador
kI = 171.122192885209
Cr = 1E-6
Re = 1/(Cr*kI)
numI = [1]
denI = [Re*Cr,0]
I = ctrl.tf(numI,denI)
print(f"Capacitancia Cr: {Cr} Faradios\n")
print(f"Resistencia Re: {Re:.3e} Ohms\n")
print(f"Función de transferencia del controlador: {I}\n")

# Sistema de control en lazo cerrado
sysI = ctrl.feedback(ctrl.series(I,sys),1,sign = -1)
print(f"Función de transferencia en lazo cerrado: {sysI}\n")

#Colores 
clr1 = np.array([(118, 196, 87)])/255
clr2 = np.array([(27, 44, 193)])/255
clr3 = np.array([(221, 113, 113)])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,Vsu = ctrl.forced_response(sys,t,u,x0)
    return Vsu
    
def closedloop(t,sysI,u):
    _,Iu = ctrl.forced_response(sysI,t,u,x0)
    return Iu

# Respuestas: Simulaciones numéricas
for i in range(0,4):
    Vsu = openloop(t,sys,u[:,i])
    Iu = closedloop(t,sysI,u[:,i])

    fg = plt.figure(i+1)
    fg.set_size_inches(w,h)

    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']

    plt.plot(t, u[:,i],
             '-', color=clr1,
             label=r'$V_e(t)$')

    plt.plot(t, Vsu,
             '--o', color=clr2,
             linewidth=1.5,
             markersize=3,
             markevery=250,
             label=r'$V_s(t)$')

    plt.plot(t, Iu,
             ':x', color=clr3,
             linewidth=2.0,
             markersize=4,
             markevery=250,
             label=r'$I(t)$')

    plt.xlim(0,10)
    plt.xticks(np.arange(0,11,1))

    if i == 0 or i == 1 or i == 2:
        plt.ylim(-0.1,1.2)
        plt.yticks(np.arange(-0.1,1.3,0.1))

    elif i == 3:
        plt.ylim(-1.2,1.2)
        plt.yticks(np.arange(-1.2,1.4,0.2))

    plt.xlabel('t [s]')
    plt.ylabel(r'$V_i(t)$ [V]')

    plt.legend(
        bbox_to_anchor=(0.5,-0.25),
        loc='center',
        ncol=3,
        frameon=False
    )

    fg.savefig(
        signals[i] + '_python1.pdf',
        bbox_inches='tight'
    )

    plt.show()