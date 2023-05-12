var chart = LightweightCharts.createChart(document.getElementById("chart"), {
  width: 1000,
  height: 500,
  layout: {
    background: {
      type: "solid",
      color: "#000000",
    },
  },
  grid: {
    vertLines: {
      visible: false,
    },
    horzLines: {
      visible: false,
    },
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
  },
  priceScale: {
    borderColor: "rgba(197, 203, 206, 0.8)",
  },
  timeScale: {
    borderColor: "rgba(197, 203, 206, 0.8)",
    timeVisible: true,
    secondsVisible: false,
  },
});

var candleSeries = chart.addCandlestickSeries({
  wickVisible: false,
  upColor: "#00ff00",
  downColor: "#ff0000",
  //borderDownColor: "rgba(255, 144, 0, 1)",
  //borderUpColor: "rgba(255, 144, 0, 1)",
  //wickDownColor: "rgba(255, 144, 0, 1)",
  //wickUpColor: "rgba(255, 144, 0, 1)",
});

fetch("http://127.0.0.1:5000/history")
  .then((r) => r.json())
  .then((response) => {
    console.log(response);

    candleSeries.setData(response);
  });

var binanceSocket = new WebSocket(
  "wss://stream.binance.com:9443/ws/btcusdt@kline_5m"
);

binanceSocket.onmessage = function (event) {
  var message = JSON.parse(event.data);

  var candlestick = message.k;

  console.log(candlestick);

  candleSeries.update({
    time: candlestick.t / 1000,
    open: candlestick.o,
    high: candlestick.h,
    low: candlestick.l,
    close: candlestick.c,
  });
};
