# Digital Sound Transfer Protocol (DSTP)

Uses a custom implementation of MFSK 4. Not even sure if I implemented it correctly, but it works. \
Example signal in `src/signals`. \
Video of CLI in `docs`. 

**Not done yet.**


Also, don't use this in the real world. It's a terrible protocol. This was made for fun.

## Statistics
<table>
  <tr>
    <th>Sampling Freq (Hz)</th>
    <td>48,000</td>
  </tr>
  <tr>
    <th>Symbol Rate (Baud)</th>
    <td>100</td>
  </tr>
  <tr>
    <th>Frequencies</th>
    <td>400, 800, 1200, 1600</td>
  </tr>
  <tr>
    <th>Symbol Map</th>
    <td>- <code>00</code>: 400<br/>- <code>01</code>: 800<br/>- <code>10</code>: 1200<br/>- <code>11</code>: 1600</td>
  </tr>
</table>
