import { useEffect, useState } from 'react';
export default function Vehiculos() {
  const [vehiculos, setVehiculos] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => {
    const controller = new AbortController();
    fetch('http://127.0.0.1:8000/api/vehiculos/', { signal: controller.signal })
      .then(r => { if (!r.ok) throw Error('Error HTTP ' + r.status); return r.json(); })
      .then(setVehiculos)
      .catch(e => { if (e.name !== 'AbortError') setError(e.message); });
    return () => controller.abort();
  }, []);
  return <><p>{error}</p><ul>{vehiculos.map(v =>
    <li key={v.id}>{v.marca} {v.modelo} - {v.anio} - {v.color}</li>)}</ul></>;
}
