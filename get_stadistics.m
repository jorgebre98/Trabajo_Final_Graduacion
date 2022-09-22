Inputs = [];
Angles = [];
prom = [];
desv = [];

for i = 1:10
  files = csvread(strcat('Data_',num2str(i),'.csv'));
  Inputs(:,i) = files(:,3);
  Angles(:,i) = files(:,4);
endfor

for i = 1:length(Angles)
  prom(:,i) = mean(Angles(i,:));
  desv(:,i) = std(Angles(i,:));
endfor

figure(1)
plot(Inputs);
title('Secuencia de entrada');
xlabel('Tiempo (ms)')

figure(2)
plot(Angles);
title('Ángulo obtenido de la PAHM');
xlabel('Tiempo (ms)')
ylabel('Ángulo (°)')
legend()

figure(3)
plot(prom);
title('Promedio de los ángulos en cada muestra');
xlabel('Tiempo (ms)')
legend()

figure(4)
plot(desv);
title('Desviación estándar de los angulos en cada muestra');
xlabel('Tiempo (ms)')
legend()

figure(5)
x = 1:numel(prom);
curve1 = prom + desv;
curve2 = prom - desv;
x2 = [x, fliplr(x)]; # vector tamaño de x y x invertido
inBetween = [curve1, fliplr(curve2)];
fill(x2, inBetween, [0.87,0.87,0.87]);
hold on;
plot(x, prom, 'k','LineWidth', 2);