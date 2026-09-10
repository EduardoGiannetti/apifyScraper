using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

public class Comentario
{
    [JsonPropertyName("message")]
    public string Text { get; set; }

    [JsonPropertyName("likeCount")]
    public int LikeCount { get; set; }
}

class Program
{
    // Partição ajustada para ordenar do MAIOR para o MENOR (Decrescente)
    public static int Particionar(List<Comentario> lista, int esquerda, int direita)
    {
        int pivo = lista[(esquerda + direita) / 2].LikeCount;
        
        while (esquerda <= direita)
        {
            // Invertido: avança enquanto o elemento atual for MAIOR que o pivô
            while (lista[esquerda].LikeCount > pivo)
            {
                esquerda++;
            }
            // Invertido: recua enquanto o elemento atual for MENOR que o pivô
            while (lista[direita].LikeCount < pivo)
            {
                direita--;
            }

            if (esquerda <= direita)
            {
                Comentario temp = lista[esquerda];
                lista[esquerda] = lista[direita];
                lista[direita] = temp;
                esquerda++;
                direita--;
            }
        }
        return esquerda;
    }

    public static void QuickSort(List<Comentario> lista, int esquerda, int direita)
    {
        if (esquerda < direita)
        {
            int posicao = Particionar(lista, esquerda, direita);
            QuickSort(lista, esquerda, posicao - 1);
            QuickSort(lista, posicao, direita);
        }
    }

    static void Main(string[] args)
    {
        // Recebe o caminho do arquivo JSON enviado pelo Python
        string filePath = args.Length > 0 ? args[0] : @"C:\Users\EduardoGiannetti\Downloads\apifymcp\json\comentarios.json";

        if (!File.Exists(filePath))
            return;

        string jsonInput = File.ReadAllText(filePath);
        var comentarios = JsonSerializer.Deserialize<List<Comentario>>(jsonInput);

        if (comentarios != null && comentarios.Count > 0)
        {
            // Executa o QuickSort em C#
            QuickSort(comentarios, 0, comentarios.Count - 1);

            // Sobrescreve o arquivo JSON com a lista já ordenada
            string jsonOrdenado = JsonSerializer.Serialize(comentarios, new JsonSerializerOptions { WriteIndented = true });
            Console.WriteLine(jsonOrdenado);
            File.WriteAllText(filePath, jsonOrdenado);
        }
    }
}