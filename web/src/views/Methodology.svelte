<section class="space-y-4">
<article class="card">
  <h3>Como o cálculo funciona</h3>
  <ol class="my-4 list-decimal pl-10">
    <li>Cada partido tem duas coordenadas: <b>econômica</b> (−10 esquerda a +10 direita) e <b>social</b> (−10 libertário a +10 autoritário), seguindo o modelo bidimensional do <a href="https://pt.wikipedia.org/wiki/Espectro_pol%C3%ADtico" target="_blank" rel="noreferrer">espectro político</a>.</li>
    <li>Para cada ano, conta-se quantas cadeiras cada partido ocupou em cada instituição, <b>proporcional aos dias em exercício</b>. Um deputado que trocou de partido em julho conta metade do ano em cada partido.</li>
    <li>A posição de uma instituição é a média das coordenadas dos seus membros.</li>
    <li>A posição do Brasil é a média das instituições ponderada pelos <b>pesos</b>, que você pode editar. Instituições sem dados no ano ficam de fora e os pesos são renormalizados.</li>
  </ol>
</article>

<article class="card">
  <h3>Fontes</h3>
  <ul class="my-4 list-disc pl-10">
    <li><b>Câmara:</b> API de Dados Abertos da Câmara dos Deputados (legislaturas 49 a 57, com o histórico de posse, afastamento e troca de partido de cada deputado).</li>
    <li><b>Senado:</b> API de Dados Abertos do Senado Federal (exercícios e filiações de cada senador).</li>
    <li><b>Governadores e deputados estaduais:</b> TSE Dados Abertos, candidatos eleitos de 1994 a 2022.</li>
    <li><b>Presidentes:</b> lista curada à mão, incluindo os períodos sem partido.</li>
  </ul>
</article>

<article class="card">
  <h3>Limitações</h3>
  <p class="text-sm text-muted">Leia antes de concluir algo.</p>
  <ul class="my-4 list-disc pl-10">
    <li><b>As coordenadas são estimativas.</b> Não existe classificação oficial. O eixo econômico pode ser calibrado com surveys de especialistas (ex.: Bolognesi, Ribeiro &amp; Codato, 2023). O eixo social não tem fonte acadêmica equivalente.</li>
    <li>O partido é usado como aproximação da posição individual. Parlamentares divergem do próprio partido.</li>
    <li>Câmara antes de 2003: a API não traz datas confiáveis de troca de partido, então vale o partido registrado na legislatura.</li>
    <li>Senado 1994: os mandatos iniciados em 1987 não têm registro de exercício nem datas de filiação na API. Conta o titular pelo mandato inteiro, com a filiação mais recente registrada.</li>
    <li>Governadores: eleições suplementares (ex.: AM 2017, TO 2018) trocam o governador na data da eleição. Vices que assumiram por renúncia ou morte não são capturados.</li>
    <li>Governadores e Assembleias em 1994: sem dados. O mandato vigente veio da eleição de 1990, fora do recorte.</li>
    <li>Deputados estaduais e governadores: vale o partido da eleição. Trocas de partido e vices que assumiram não são capturados.</li>
    <li>Fusões não reescrevem o passado: um deputado do PFL em 2005 conta como PFL/DEM, não como União Brasil.</li>
    <li>Posição ideológica não mede competência nem resultado de governo.</li>
  </ul>
</article>
</section>
