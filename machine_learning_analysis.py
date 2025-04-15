import React, { useState, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import axios from "axios";
import { DataTable } from "@/components/ui/data-table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const columns = [
  { accessorKey: "ano_mes", header: "Ano Mês" },
  { accessorKey: "cnpj_distribuidor", header: "CNPJ Distribuidor" },
  { accessorKey: "nome_distribuidor", header: "Nome do Distribuidor" },
  { accessorKey: "cnpj_cliente", header: "CNPJ/CPF Cliente" },
  { accessorKey: "nome_cliente", header: "Nome do Cliente" },
  { accessorKey: "ramo", header: "Ramo" },
  { accessorKey: "ean", header: "EAN" },
  { accessorKey: "quantidade_kg", header: "Qtd Vendida Kg" },
  { accessorKey: "volume_caixas", header: "Volume Caixas" },
  { accessorKey: "volume_ton", header: "Volume Ton" },
  { accessorKey: "faturamento", header: "Faturamento" },
  { accessorKey: "regional", header: "Regional" },
  { accessorKey: "cidade", header: "Cidade" },
  { accessorKey: "estado", header: "Estado" },
  { accessorKey: "representatividade_volume", header: "% Represent." },
];

const PainelJDE = () => {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<any[]>([]);
  const [filtros, setFiltros] = useState({
    ano_mes: "",
    estado: "",
    cidade: "",
    regional: "",
    nome_distribuidor: "",
    nome_cliente: ""
  });

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload-excel/", formData);
      setData(res.data.data);
    } catch (err) {
      console.error("Erro no upload:", err);
    }
  };

  const dadosFiltrados = useMemo(() => {
    return data.filter((item) => {
      return (
        (!filtros.ano_mes || item.ano_mes == filtros.ano_mes) &&
        (!filtros.estado || item.estado === filtros.estado) &&
        (!filtros.cidade || item.cidade === filtros.cidade) &&
        (!filtros.regional || item.regional === filtros.regional) &&
        (!filtros.nome_distribuidor || item.nome_distribuidor === filtros.nome_distribuidor) &&
        (!filtros.nome_cliente || item.nome_cliente === filtros.nome_cliente)
      );
    });
  }, [data, filtros]);

  const valoresUnicos = (chave: string) => {
    return [...new Set(data.map((d) => d[chave]).filter(Boolean))];
  };

  return (
    <div className="p-8 bg-[url('/cafe-fundo.jpg')] bg-cover min-h-screen font-sans">
      <Card className="max-w-6xl mx-auto p-6 rounded-2xl shadow-2xl backdrop-blur-md bg-white/80">
        <CardHeader>
          <h1 className="text-3xl font-bold mb-6 text-center text-[#4e342e]">Painel JDE COFFEE</h1>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 justify-between mb-6">
            <Input type="file" accept=".xlsx" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            <Button onClick={handleUpload}>Enviar Excel</Button>
          </div>

          <Tabs defaultValue="tabela" className="w-full">
            <TabsList className="mb-6">
              <TabsTrigger value="tabela">Tabela Dinâmica</TabsTrigger>
              <TabsTrigger value="graficos">Gráficos</TabsTrigger>
            </TabsList>

            <TabsContent value="tabela">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <Select onValueChange={(v) => setFiltros({ ...filtros, ano_mes: v })}>
                  <SelectTrigger>Ano Mês</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("ano_mes").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select onValueChange={(v) => setFiltros({ ...filtros, estado: v })}>
                  <SelectTrigger>Estado</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("estado").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select onValueChange={(v) => setFiltros({ ...filtros, cidade: v })}>
                  <SelectTrigger>Cidade</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("cidade").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select onValueChange={(v) => setFiltros({ ...filtros, regional: v })}>
                  <SelectTrigger>Regional</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("regional").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select onValueChange={(v) => setFiltros({ ...filtros, nome_distribuidor: v })}>
                  <SelectTrigger>Distribuidor</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("nome_distribuidor").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select onValueChange={(v) => setFiltros({ ...filtros, nome_cliente: v })}>
                  <SelectTrigger>Cliente</SelectTrigger>
                  <SelectContent>
                    {valoresUnicos("nome_cliente").map((v, i) => (
                      <SelectItem key={i} value={v}>{v}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              {dadosFiltrados.length > 0 && (
                <DataTable columns={columns} data={dadosFiltrados} />
              )}
            </TabsContent>

            <TabsContent value="graficos">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="p-4 bg-white/70 shadow-md">
                  <h2 className="text-lg font-semibold text-center mb-2">Faturamento</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={dadosFiltrados}>
                      <XAxis dataKey="nome_distribuidor" hide />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="faturamento" fill="#6f4e37" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
                <Card className="p-4 bg-white/70 shadow-md">
                  <h2 className="text-lg font-semibold text-center mb-2">Volume por Toneladas</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={dadosFiltrados}>
                      <XAxis dataKey="nome_distribuidor" hide />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="volume_ton" fill="#8d6e63" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default PainelJDE;
