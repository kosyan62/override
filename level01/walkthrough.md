After long exploration I wrote couple of helpers.
Python script will help to generate payload for gdb reserching and actual attack.
main.c should be compilled with `gcc -m 32 main.c -o /tmp/a`. In this case
our binary will be able to run with execve from exploited program.
