'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'

export default function AdminPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const userStr = localStorage.getItem('user')
    if (!userStr) {
      router.push('/login')
      return
    }
    const userData = JSON.parse(userStr)
    if (!userData.is_admin) {
      router.push('/dashboard')
      return
    }
    setUser(userData)
  }, [router])

  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const response = await api.get('/analytics/dashboard')
      return response.data
    },
  })

  if (!user) {
    return <div>Загрузка...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Админ-панель</h1>

        {isLoading ? (
          <div>Загрузка...</div>
        ) : analytics ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm text-gray-600 mb-2">Всего обращений</h3>
              <p className="text-3xl font-bold text-gray-900">{analytics.total_appeals}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm text-gray-600 mb-2">Процент решенных</h3>
              <p className="text-3xl font-bold text-green-600">{analytics.resolution_rate.toFixed(1)}%</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm text-gray-600 mb-2">Среднее время решения</h3>
              <p className="text-3xl font-bold text-blue-600">{analytics.average_resolution_time.toFixed(1)}ч</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm text-gray-600 mb-2">Ожидают</h3>
              <p className="text-3xl font-bold text-yellow-600">
                {analytics.appeals_by_status?.pending || 0}
              </p>
            </div>
          </div>
        ) : null}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Статистика по категориям</h2>
          {analytics?.appeals_by_category && (
            <div className="space-y-2">
              {Object.entries(analytics.appeals_by_category).map(([category, count]) => (
                <div key={category} className="flex justify-between">
                  <span className="text-gray-700">{category}</span>
                  <span className="font-semibold">{count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

