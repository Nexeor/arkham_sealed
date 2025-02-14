import apiClient from "../services/api-client.ts"
import { AxiosRequestConfig, CanceledError } from "axios"
import { useEffect, useState } from "react";

interface FetchResponse<T> {
  cards: T[],
}

const useData = <T>(endpoint : string, requestConfig?: AxiosRequestConfig, deps?: any[]) => {
      const [data, setData] = useState<T[]>([]);
      const [error, setError] = useState("");
      const [isLoading, setLoading] = useState(false)
    
      useEffect(() => {
        const controller = new AbortController();
        setLoading(true)
        apiClient
          .get<FetchResponse<T>>(endpoint, { signal : controller.signal, ...requestConfig})
          .then((res) => {
            console.log("API Response:", res.data)
            setData(res.data.cards);
            setLoading(false)
          })
          .catch((err) => {
            if (err instanceof CanceledError) return;
            setError(err.message);
            setLoading(false)
          })
          return () => controller.abort();
      }, deps ? [...deps] : []);


      return { data, error, isLoading }
    }

    
    export default useData;