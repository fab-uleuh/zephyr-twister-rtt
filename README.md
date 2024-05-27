# zephyr-twister-rtt

This script allows you to launch Twister through RTT.

```bash
./scripts/twister <your option> --device-testing --west-flash="--erase" --west-runner nrfjprog   --device-serial-pty ./rtt.py
```

## Sample with custom bord

```bash
./scripts/twister --board-root <path-board>  --extra-args=BOARD_ROOT=<path-board>  -k --device-testing --west-flash="--erase" --west-runner nrfjprog   --device-serial-pty ./rtt.py
```