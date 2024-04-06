# Digital Sound Transfer Protocol (DSTP)

Uses custom implementation of MFSK. Not even sure if I implemented it correctly, but it works. \
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
    <td>- `00`: 400<br/>- `01`: 800<br/>- `10`: 1200<br/>- `11`: 1600</td>
  </tr>
</table>
