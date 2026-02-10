const firebaseConfig = {
  apiKey: "SUA_API_KEY_AQUI",
  authDomain: "SEU_PROJETO.firebaseapp.com",
  databaseURL: "https://SEU_PROJETO.firebaseio.com",
  projectId: "SEU_PROJETO",
  storageBucket: "SEU_PROJETO.appspot.com",
  messagingSenderId: "ID_AQUI",
  appId: "APP_ID_AQUI"
};

// Inicializa o Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();

let carrinho = [];
let total = 0;

function adicionarAoCarrinho(nome, preco) {
    carrinho.push(nome);
    total += preco;
    document.getElementById("itens-carrinho").innerText = carrinho.join(", ");
    document.getElementById("total").innerText = `Total: R$ ${total.toFixed(2)}`;
}

function finalizarPedido() {
    const nome = document.getElementById("nome").value;
    const end = document.getElementById("endereco").value;
    const pag = document.getElementById("pagamento").value;
    const bairro = document.getElementById("bairro").value;

    if (!nome || !end) {
        alert("Preencha nome e endereço!");
        return;
    }

    const formas = {"1": "PIX", "2": "DINHEIRO", "3": "CARTÃO"};
    const tagPag = formas[pag];

    const pedido = {
        cliente: `${nome} (${tagPag})`,
        lanche: carrinho.join(", "),
        total: total,
        endereco: end,
        bairro: bairro,
        status: "PREPARANDO",
        hora_entrada: new Date().toLocaleString('pt-BR')
    };

    database.ref('pedidos').push(pedido)
        .then(() => {
            alert("✅ Pedido enviado! Bilu já recebeu na chapa!");
            window.location.reload();
        });
}