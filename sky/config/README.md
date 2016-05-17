# Configuração do Raspberry Pi
Os ficheiros nesta pasta servem para configurar o próprio computador.

- `sky.service` é um ficheiro criado na pasta `/lib/systemd/system/` para iniciar o nosso
  software automaticamente quando se liga o computador.
- `config.txt` é o ficheiro que presente na pasta `/boot/`
- `watchdog.conf` é a configuração do watchdog e é colocado em `/etc/`
- `ntp.conf`, analogamente, é a configuração do NTP e é também colocado na pasta `/etc/`
- `cmdline-ip.txt` e `cmdline-noip.txt` são ficheiros para substituir o `/boot/cmdline.txt`
para usar um IP estático ou não; no dia do lançamento tiramos o IP estático para termos um
boot mais rápido
