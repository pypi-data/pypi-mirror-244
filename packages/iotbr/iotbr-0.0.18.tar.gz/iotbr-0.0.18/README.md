# Imput Output Tables to Brazil IOTBR

Generate **I O - T A B L E** IOTBR.

## Instructions


```python
! pip install iotbr==0.0.3

from iotbr import tru as tru
from iotbr import tru_pb as tru_pb
```

    Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/
    Collecting iotbr==0.0.3
      Downloading iotbr-0.0.3-py3-none-any.whl (7.2 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m7.2/7.2 MB[0m [31m38.7 MB/s[0m eta [36m0:00:00[0m
    [?25hRequirement already satisfied: xlrd in /usr/local/lib/python3.10/dist-packages (from iotbr==0.0.3) (2.0.1)
    Installing collected packages: iotbr
    Successfully installed iotbr-0.0.3



```python
#ler uma variável qualquer dentro da tru
tru.read_var()
```





  <div id="df-804688f7-1f60-4742-b054-7c72d883e30b">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PT</th>
    </tr>
    <tr>
      <th>produtos</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Arroz, trigo e outros cereais</th>
      <td>12631</td>
    </tr>
    <tr>
      <th>Milho em grão</th>
      <td>43663</td>
    </tr>
    <tr>
      <th>Algodão herbáceo, outras fibras da lav. temporária</th>
      <td>18376</td>
    </tr>
    <tr>
      <th>Cana-de-açúcar</th>
      <td>57068</td>
    </tr>
    <tr>
      <th>Soja  em grão</th>
      <td>153331</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>Serviços de artes, cultura, esporte e recreação</th>
      <td>45636</td>
    </tr>
    <tr>
      <th>Organizações patronais, sindicais e outros serviços associativos</th>
      <td>93816</td>
    </tr>
    <tr>
      <th>Manutenção de computadores, telefones e objetos domésticos</th>
      <td>33107</td>
    </tr>
    <tr>
      <th>Serviços pessoais</th>
      <td>62283</td>
    </tr>
    <tr>
      <th>Serviços domésticos</th>
      <td>75158</td>
    </tr>
  </tbody>
</table>
<p>128 rows × 1 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-804688f7-1f60-4742-b054-7c72d883e30b')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-804688f7-1f60-4742-b054-7c72d883e30b button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-804688f7-1f60-4742-b054-7c72d883e30b');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>





```python
#ler uma variável específica
tru.read_var('2019','68','MG_tra')
```





  <div id="df-a86d51f5-4ce0-4242-b2c3-a6892af845fc">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MG_tra</th>
    </tr>
    <tr>
      <th>produtos</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Arroz, trigo e outros cereais</th>
      <td>1405</td>
    </tr>
    <tr>
      <th>Milho em grão</th>
      <td>2631</td>
    </tr>
    <tr>
      <th>Algodão herbáceo, outras fibras da lav. temporária</th>
      <td>370</td>
    </tr>
    <tr>
      <th>Cana-de-açúcar</th>
      <td>2996</td>
    </tr>
    <tr>
      <th>Soja  em grão</th>
      <td>3433</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>Serviços de artes, cultura, esporte e recreação</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Organizações patronais, sindicais e outros serviços associativos</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Manutenção de computadores, telefones e objetos domésticos</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Serviços pessoais</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Serviços domésticos</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>128 rows × 1 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-a86d51f5-4ce0-4242-b2c3-a6892af845fc')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-a86d51f5-4ce0-4242-b2c3-a6892af845fc button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-a86d51f5-4ce0-4242-b2c3-a6892af845fc');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>





```python
#ler ler a variável com preços do ano anterior
tru.read_var('2019','68','MG_tra','t-1')
```





  <div id="df-d740900e-1799-4c36-923a-e761bfa570df">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MG_tra</th>
    </tr>
    <tr>
      <th>produtos</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Arroz, trigo e outros cereais</th>
      <td>1322</td>
    </tr>
    <tr>
      <th>Milho em grão</th>
      <td>2385</td>
    </tr>
    <tr>
      <th>Algodão herbáceo, outras fibras da lav. temporária</th>
      <td>365</td>
    </tr>
    <tr>
      <th>Cana-de-açúcar</th>
      <td>2875</td>
    </tr>
    <tr>
      <th>Soja  em grão</th>
      <td>3089</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>Serviços de artes, cultura, esporte e recreação</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Organizações patronais, sindicais e outros serviços associativos</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Manutenção de computadores, telefones e objetos domésticos</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Serviços pessoais</th>
      <td>0</td>
    </tr>
    <tr>
      <th>Serviços domésticos</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>128 rows × 1 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-d740900e-1799-4c36-923a-e761bfa570df')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-d740900e-1799-4c36-923a-e761bfa570df button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-d740900e-1799-4c36-923a-e761bfa570df');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>





```python
#ler ler a variável com outro nível e ano
tru.read_var('2000','12')
```





  <div id="df-b985967a-f875-488f-96a9-618e391cc619">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PT</th>
    </tr>
    <tr>
      <th>produtos</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Agropecuária</th>
      <td>87128.07773</td>
    </tr>
    <tr>
      <th>Indústrias extrativas</th>
      <td>35555.283895</td>
    </tr>
    <tr>
      <th>Indústrias de transformação</th>
      <td>648818.483278</td>
    </tr>
    <tr>
      <th>Eletricidade e gás, água, esgoto, atividades de gestão de resíduos</th>
      <td>64680.645095</td>
    </tr>
    <tr>
      <th>Construção</th>
      <td>146016.177837</td>
    </tr>
    <tr>
      <th>Comércio</th>
      <td>143766.942246</td>
    </tr>
    <tr>
      <th>Transporte, armazenagem e correio</th>
      <td>88682.618478</td>
    </tr>
    <tr>
      <th>Informação e comunicação</th>
      <td>86607.823103</td>
    </tr>
    <tr>
      <th>Atividades financeiras, de seguros e serviços relacionados</th>
      <td>105414.172763</td>
    </tr>
    <tr>
      <th>Atividades imobiliárias</th>
      <td>151048.781496</td>
    </tr>
    <tr>
      <th>Outras atividades de serviços</th>
      <td>320282.96256</td>
    </tr>
    <tr>
      <th>Administração, defesa, saúde e educação públicas e seguridade social</th>
      <td>209734.795687</td>
    </tr>
  </tbody>
</table>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-b985967a-f875-488f-96a9-618e391cc619')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>

  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-b985967a-f875-488f-96a9-618e391cc619 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-b985967a-f875-488f-96a9-618e391cc619');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>





```python
#encontrar matrizes de demanda final (mE) e demanda total (mU) a preços básicos
#usando o métrodo do Prof. Dr. Guilhoto
mU = tru_pb.D_total_pb('2019','68')[0]
mE = tru_pb.D_total_pb('2019','68')[1]
mE[1,:]
```




    array([22855.033437625632, 0.0, 0.0, 3492.9691568353433, 0.0, -481.0],
          dtype=object)




```python
#Estimar matriz a preços básicos para anos e níveis diferente
mU = tru_pb.D_total_pb('2010','20')[0]
mE = tru_pb.D_total_pb('2010','20')[1]
mE[1,:]
```




    array([76824.77308806025, 0.0, 0.0, 0.0, 6221.934829327755, -875.0],
          dtype=object)




```python
#Estimar matriz a preços básicos para anos, níveis e unidades diferentes
mU = tru_pb.D_total_pb('2010','51','t-1')[0]
mE = tru_pb.D_total_pb('2010','51','t-1')[1]
mU.shape
```




    (107, 51)




```python
#estimar a matrizes do sistema IO
import numpy as np
year = '2019'
level = '68'
unit = 't'
mU = tru_pb.D_total_pb(year,level,unit)[0]
mE = tru_pb.D_total_pb(year,level,unit)[1]


#Estimar matriz (D)
mV = tru.read_var(year,level,'P_matrix',unit).values.T
#Total produzido por produto
#vQ = np.sum(mV, axis=0)
vQ = tru.read_var(year,level,'PT',unit).values
mQChapeu = np.diagflat(1/vQ)
mD = np.dot(mV, mQChapeu)

#Estimar matriz (B)
#Total produzido por setor
vVBP = np.sum(mV, axis=1)
vX = np.copy(vVBP)
mXChapeu = np.diagflat(1/vX)
mB=np.dot(mU,mXChapeu)

mA = np.dot(mD,mB).astype(float)
mY = np.dot(mD,mE).astype(float)
mZ = np.dot(mD,mU).astype(float)
mI = np.eye(int(level))
 
mLeontief = np.linalg.inv(mI - mA)

mLeontief
```




    array([[1.02795846e+00, 6.63434968e-02, 1.55683119e-02, ...,
            2.48657115e-03, 8.87445164e-03, 0.00000000e+00],
           [3.46679411e-03, 1.05066335e+00, 7.50231026e-03, ...,
            5.04707964e-04, 2.99970714e-03, 0.00000000e+00],
           [4.65358841e-03, 1.14566016e-02, 1.06662450e+00, ...,
            3.39112179e-04, 7.04559555e-04, 0.00000000e+00],
           ...,
           [2.57040133e-04, 4.90720175e-04, 2.96567252e-04, ...,
            1.02021266e+00, 6.72567669e-03, 0.00000000e+00],
           [1.72661929e-03, 1.85442303e-03, 1.52402071e-03, ...,
            3.19760462e-03, 1.00595709e+00, 0.00000000e+00],
           [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, ...,
            0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])



#Variáveis que o pkg iotbr reconhece dentro da tru
- níveis 20 e 68 so tem dados a partir de 2010
-níveis 12 e 51 passaram a agregar exportações e importações a partir de 2010

![image.png](data:image/png;base64,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)
