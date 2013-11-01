% dt = .001;
% fs = 1./dt;
% numd = .03*[1 1]; % from butterworth design
% dend = [1 -.9390625];

fs = 1000;
tau = .1;

num = 1;
den = [tau, 1];
[numd,dend]=bilinear(num,den,fs,470)

[h, f] = freqz(numd,dend,100000, fs);

% plotting
figure(1); clf();
subplot(211); semilogx(f,20*log10(abs(h))); hold on
plot([.1, 1000], [-3 -3],'r'); 
grid on; ylim([-40,1]); ylabel('gain (db)'); xlim([.1, fs/2]);
subplot(212); semilogx(f, angle(h)*180/pi); 
grid on; ylabel('phase(rad)'); xlim([.1, fs/2]); xlabel('frequency(Hz)');

% figure(2); clf();
% subplot(211);
% w = linspace(0.1,fs/2, 1000);
% s = 1./(1+tau*j*w);
% semilogx(w, 20*log10(abs(s))); hold on;
% plot([.1, fs/2], [-3 -3]);
% grid on;
% title('Expected LPF bode plot');
% subplot(212);
% semilogx(w, angle(s)*180/pi);
% grid on;