
function varnome() {
    console.log("Ativou")
  var nome = document.getElementById('nome_completo').value;
  
  // Faça uma solicitação AJAX para verificar_nome
  fetch('/verificar_nome?nome=' + nome)
      .then(function(response) {
          return response.json();
      })
      .then(function(data) {
          // Preencha os campos do formulário com os dados retornados
          document.getElementById('email').value = data.email || '';
          document.getElementById('cpf').value = data.cpf || '';
          document.getElementById('celular').value = data.celular || '';
          document.getElementById('telefone').value = data.telefone || '';
          document.getElementById('whatsapp').value = data.whatsapp || '';
          document.getElementById('endereco').value = data.endereco || '';
          document.getElementById('observacao').value = data.observacao || '';
          document.getElementById('cep').value = data.cep || '';
      });
}

