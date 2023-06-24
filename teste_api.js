const Binance = require("node-binance-api");
const binance = new Binance().options({
  APIKEY: "8a412e31318c09a430bee5de96043486634b17184d4648fc9ae765ee3c8cebeb",
  APISECRET: "0a52773db460caac3e07599de446049a28f171475ff813bf06a7be5eba168b68",
  useServerTime: true,
  test: true, // Habilita o modo Testnet
});

// Função assíncrona para obter e imprimir os dados da conta
async function obterDadosConta() {
  try {
    const accountInfo = await binance.futuresAccount();

    console.log("Dados da conta:");
    console.log(accountInfo);
  } catch (error) {
    console.error("Erro ao obter os dados da conta:", error);
  }
}

// Chama a função assíncrona para obter os dados da conta
obterDadosConta();