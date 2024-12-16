'use client'; 

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface QueryResult {
    id: number;
    source_address: string;
    destination_address: string;
    distance: number;
  }
  
const API_BASE = "https://deliverydist-api.fly.dev"

const DistanceCalculator = () => {
  const [sourceAddress, setSourceAddress] = useState('');
  const [destinationAddress, setDestinationAddress] = useState('');
  const [history, setHistory] = useState<QueryResult[]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/queries/`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        redirect: 'follow', 
      });
      
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error('Detailed error:', error);
      setError(`Failed to fetch search history: ${error}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setLoading(true);
      setError('');
      setResult(null);

      try {
        const response = await fetch(`${API_BASE}/api/v1/queries/`, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          redirect: 'follow', 
          body: JSON.stringify({
            source_address: sourceAddress,
            destination_address: destinationAddress,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Failed to calculate distance');
        }

        setResult(data);
        await fetchHistory();
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('An unknown error occurred');
        }
      } finally {
        setLoading(false);
      }
  };

  return (
    <div className="mx-auto max-w-2xl p-4 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Distance Calculator</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input
                placeholder="Source Address"
                value={sourceAddress}
                onChange={(e) => setSourceAddress(e.target.value)}
                required
              />
            </div>
            <div>
              <Input
                placeholder="Destination Address"
                value={destinationAddress}
                onChange={(e) => setDestinationAddress(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Calculating...' : 'Calculate Distance'}
            </Button>
          </form>

          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {result && (
            <Alert className="mt-4">
              <AlertDescription>
                Distance: {result.distance} kilometers
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Search History</CardTitle>
        </CardHeader>
        <CardContent>
            <div className="space-y-2">
                {history && history.length > 0 ? (
                history.map((query) => (
                    <div
                    key={query.id}
                    className="p-4 rounded-lg border border-gray-200"
                    >
                    <p className="text-sm text-gray-600">
                        From: {query.source_address}
                    </p>
                    <p className="text-sm text-gray-600">
                        To: {query.destination_address}
                    </p>
                    <p className="text-sm font-medium">
                        Distance: {query.distance} km
                    </p>
                    </div>
                ))
                ) : (
                <p className="text-sm text-gray-500">No search history available</p>
                )}
            </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DistanceCalculator;