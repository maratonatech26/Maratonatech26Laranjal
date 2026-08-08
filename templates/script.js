let textoPrompt = document.getElementById('inputPrompt');
let arquivoImagem = document.getElementById('inputImage');
let printText = document.getElementById('respostaApiText');
printText.innerHTML=`<h1 class="resposta">FIQUE ATENTOE FAÇA UMA BUSCA</h1>`;
//push
async function enviarParaServidor(arquivoImagem, textoPrompt) {
  const formData = new FormData();
  
  // 'imagem' e 'texto' devem bater com os nomes esperados no Flask (request.files / request.form)
  formData.append('imagem', arquivoImagem); 
  formData.append('texto', textoPrompt);

  try {
    const response = await fetch('http://localhost:5000/analisar', {
      method: 'POST',
      body: formData // Não defina Content-Type manualmente aqui, o navegador faz isso sozinho
    });

    const resultado = await response.json();
    
    if (resultado.sucesso) {
    printText.innerHTML=`<p class="resposta">${resultado.analise}</p>`
    } else {
      printText.innerHTML=`<p class="resposta">${resultado.erro}</p>`
    }
  } catch (error) {
printText.innerHTML=`<p class="resposta">Erro de conexão com Flask</p>`
  }
}
