<script>
  const OFFICES = [
    {
      name: 'Presidente da República',
      count: '1 · mandato de 4 anos · 1 reeleição consecutiva',
      does: [
        'Chefe de Estado e de Governo: dirige a administração federal e nomeia ministros.',
        'Sanciona ou veta leis aprovadas pelo Congresso.',
        'Edita medidas provisórias: têm força de lei por até 120 dias, mas caducam se o Congresso não aprovar.',
        'Envia a proposta de orçamento (PLOA) e executa o orçamento aprovado.',
        'Indica ministros do STF, o PGR e a diretoria do Banco Central, todos com aprovação do Senado. Comanda as Forças Armadas.',
      ],
      doesNot: [
        'Não cria lei sozinho: toda lei passa pelo Congresso, e o veto pode ser derrubado por maioria absoluta das duas Casas.',
        'Não cria nem aumenta imposto sem lei. As exceções são alíquotas de IPI, IOF e impostos de importação e exportação.',
        'Não gasta fora do orçamento aprovado pelo Congresso. As emendas parlamentares individuais e de bancada são de execução obrigatória.',
        'Não controla segurança pública, saúde e educação de estados e municípios.',
      ],
    },
    {
      name: 'Deputado Federal',
      count: '513 · mandato de 4 anos · proporcional à população (8 a 70 por estado)',
      does: [
        'Propõe, emenda e vota leis federais, incluindo as de imposto, trabalho, penais e previdência.',
        'Aprova emendas à Constituição: 3/5 dos votos em dois turnos.',
        'Autoriza a abertura de impeachment do presidente (2/3 dos votos).',
        'Vota o orçamento e destina emendas parlamentares.',
        'Fiscaliza o Executivo: CPIs, convocação de ministros, TCU. A Câmara decide o que entra em pauta, o que dá muito poder ao seu presidente.',
      ],
      doesNot: [
        'Não executa obras nem serviços: indica recursos, quem executa é o governo.',
        'Não governa estados ou municípios.',
      ],
    },
    {
      name: 'Senador',
      count: '81 · 3 por estado · mandato de 8 anos (renova 1/3 e 2/3 alternadamente)',
      does: [
        'Revisa e vota as leis vindas da Câmara e propõe as próprias.',
        'Julga o presidente no impeachment (2/3 para condenar).',
        'Aprova ministros do STF, o PGR, a diretoria do Banco Central e embaixadores.',
        'Fixa limites de endividamento da União, estados e municípios.',
      ],
      doesNot: [
        'Não executa políticas públicas.',
        'Não abre processo de impeachment: isso cabe à Câmara.',
      ],
    },
    {
      name: 'Governador',
      count: '27 (26 estados + DF) · mandato de 4 anos · 1 reeleição',
      does: [
        'Comanda a segurança pública: Polícia Militar, Polícia Civil e sistema prisional estadual.',
        'Gere hospitais estaduais e a rede do ensino médio.',
        'Administra o ICMS, o imposto de maior arrecadação do país, e o IPVA. Cuida das rodovias estaduais.',
        'Sanciona ou veta leis estaduais.',
      ],
      doesNot: [
        'Não legisla sobre direito penal, trabalhista ou civil: isso é competência da União.',
        'Não define a política econômica: juros e câmbio são do Banco Central e da União.',
      ],
    },
    {
      name: 'Deputado Estadual',
      count: '1.059 no total · 4 anos · de 24 a 94 por Assembleia (CF art. 27)',
      does: [
        'Propõe e vota leis estaduais e o orçamento do estado.',
        'Fiscaliza o governador e pode abrir impeachment estadual.',
        'Aprova conselheiros do Tribunal de Contas do Estado.',
      ],
      doesNot: [
        'Não legisla sobre temas da União (penal, trabalhista, imposto federal).',
        'Não executa obras nem serviços.',
      ],
    },
  ]
</script>

<section class="space-y-4">
  <p class="text-ink-2">
    Cada cargo tem poder diferente sobre o dia a dia do cidadão. O Presidente não governa sozinho: depende do
    Congresso para aprovar leis e orçamento, e os governadores cuidam de boa parte dos serviços que a população mais
    usa. Prefeitos e vereadores (saúde básica, creche, transporte e zoneamento) e o STF (não eleito) ficam fora deste
    recorte.
  </p>

  <section class="card" aria-labelledby="axes-title">
    <h3 id="axes-title">Como ler o espectro</h3>
    <p class="mb-3 text-muted">
      O espectro usa dois eixos independentes. Uma pessoa ou partido pode ser de direita na economia e libertário
      nos costumes, ou de esquerda na economia e autoritário, por exemplo. Nenhum polo é "certo" ou "errado": o eixo
      descreve prioridades diferentes.
    </p>

    <div class="grid gap-6 min-[721px]:grid-cols-2">
      <article>
        <h4 class="mt-4 mb-1">Eixo econômico: esquerda ↔ direita</h4>
        <p class="mb-2 text-ink-2">Qual deve ser o papel do Estado na economia?</p>
        <dl class="[&_dd]:mt-0.5 [&_dt]:mt-2 [&_dt]:font-semibold">
          <dt>Esquerda</dt>
          <dd>
            Mais Estado na economia: impostos progressivos para redistribuir renda, serviços públicos amplos (saúde,
            educação, previdência), empresas estatais em setores estratégicos, direitos trabalhistas mais fortes.
          </dd>
          <dt>Direita</dt>
          <dd>
            Mais mercado: impostos e gastos públicos menores, privatizações, menos regulação, responsabilidade fiscal,
            relações de trabalho mais flexíveis. É o que no Brasil se costuma chamar de <b>liberalismo econômico</b>.
          </dd>
          <dt>Centro</dt>
          <dd>Combina elementos dos dois lados. No gráfico, é a região perto do zero.</dd>
        </dl>
      </article>

      <article>
        <h4 class="mt-4 mb-1">Eixo social: autoritário ↔ libertário</h4>
        <p class="mb-2 text-ink-2">Quanto o Estado deve controlar a vida e o comportamento das pessoas?</p>
        <dl class="[&_dd]:mt-0.5 [&_dt]:mt-2 [&_dt]:font-semibold">
          <dt>Autoritário</dt>
          <dd>
            Prioriza ordem, autoridade e tradição: mais poder para polícia e punição, controle sobre costumes e
            expressão, hierarquia e valores coletivos acima das escolhas individuais.
          </dd>
          <dt>Libertário</dt>
          <dd>
            Prioriza liberdades individuais: menos interferência do Estado na vida privada, liberdade de expressão e
            de costumes, direitos civis e garantias contra o poder do Estado.
          </dd>
          <dt>Atenção ao termo</dt>
          <dd>
            "Libertário" aqui não é "liberal". Liberal, no Brasil, geralmente descreve a posição econômica (direita);
            libertário descreve a posição social.
          </dd>
        </dl>
      </article>
    </div>

    <h4 class="mt-4 mb-1">Os quatro quadrantes</h4>
    <div class="grid max-w-140 grid-cols-2 gap-0.5 overflow-hidden rounded-lg [&>div]:flex [&>div]:flex-col [&>div]:gap-0.5 [&>div]:p-3 min-[721px]:[&>div]:aspect-[2/1] [&_span]:text-[0.9rem] [&_span]:text-ink-2">
      <div class="bg-q-auth-left"><b>Esquerda autoritária</b><span>Estado forte na economia e nos costumes.</span></div>
      <div class="bg-q-auth-right"><b>Direita autoritária</b><span>Mercado livre com ordem e valores tradicionais.</span></div>
      <div class="bg-q-lib-left"><b>Esquerda libertária</b><span>Estado forte na economia, liberdade nos costumes.</span></div>
      <div class="bg-q-lib-right"><b>Direita libertária</b><span>Pouco Estado na economia e nos costumes.</span></div>
    </div>
    <p class="mt-4 text-sm text-muted">
      Baseado no modelo bidimensional do
      <a href="https://pt.wikipedia.org/wiki/Espectro_pol%C3%ADtico" target="_blank" rel="noreferrer">espectro político</a>.
      As posições dos partidos no app são estimativas editáveis na aba <a href="#settings">Pesos e partidos</a>.
    </p>
  </section>

  <div class="grid gap-4 min-[721px]:grid-cols-2">
    {#each OFFICES as c}
      <article class="card [&_h4]:mt-3 [&_h4]:mb-1 [&_h4]:text-[0.9rem] [&_h4]:text-ink-2 [&_ul]:list-disc [&_ul]:pl-4.5">
        <h3>{c.name}</h3>
        <p class="text-muted">{c.count}</p>
        <h4>O que faz</h4>
        <ul>{#each c.does as f}<li>{f}</li>{/each}</ul>
        <h4>O que não faz</h4>
        <ul>{#each c.doesNot as f}<li>{f}</li>{/each}</ul>
      </article>
    {/each}
  </div>
</section>
