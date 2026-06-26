// export default {
//     formatarNumero2Casas,
//     formatarMoedaBR,
//     parseDataAPI,
//     formatarDataBR,
// };

export const formatarNumero2Casas = (value) => {
  if (value == null) return '';
  return value.toFixed(2);
}

export const formatarMoedaBR = (value) => {
  if (value == null) return '';
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

export const parseDataAPI = (value) => {
  if (!value) return null;
  return new Date(`${value}T00:00:00`);
};

export const formatarDataBR = (value) => {
  if (!value) return '';
  return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(value);
};