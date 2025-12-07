'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Appeal, AppealStatus, AppealCategory } from '@/lib/types'
import { Button } from '@/components/ui/button'

const statusLabels: Record<AppealStatus, string> = {
  [AppealStatus.PENDING]: 'Ожидает',
  [AppealStatus.IN_PROGRESS]: 'В работе',
  [AppealStatus.RESOLVED]: 'Решено',
  [AppealStatus.REJECTED]: 'Отклонено',
  [AppealStatus.CLOSED]: 'Закрыто',
}

const categoryLabels: Record<AppealCategory, string> = {
  [AppealCategory.ROADS]: 'Дороги и транспорт',
  [AppealCategory.LIGHTING]: 'Освещение',
  [AppealCategory.IMPROVEMENT]: 'Благоустройство',
  [AppealCategory.ECOLOGY]: 'Экология и отходы',
  [AppealCategory.SAFETY]: 'Безопасность',
  [AppealCategory.HEALTHCARE]: 'Здравоохранение',
  [AppealCategory.UTILITIES]: 'Коммунальные услуги',
  [AppealCategory.SOCIAL]: 'Социальная помощь',
  [AppealCategory.OTHER]: 'Другое',
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const userStr = localStorage.getItem('user')
    if (!userStr) {
      router.push('/login')
      return
    }
    setUser(JSON.parse(userStr))
  }, [router])

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['appeals'],
    queryFn: async () => {
      const response = await api.get<{ items: Appeal[]; total: number }>('/appeals')
      return response.data
    },
  })

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/')
  }

  if (!user) {
    return <div>Загрузка...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">Г</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">Глас</span>
          </Link>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">{user.full_name}</span>
            {user.is_admin && (
              <Link href="/admin">
                <Button variant="outline">Админ-панель</Button>
              </Link>
            )}
            <Button variant="ghost" onClick={handleLogout}>
              Выход
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Мои обращения</h1>
          <Link href="/appeals/create">
            <Button>Создать обращение</Button>
          </Link>
        </div>

        {isLoading ? (
          <div className="text-center py-12">Загрузка...</div>
        ) : data?.items.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-600 mb-4">У вас пока нет обращений</p>
            <Link href="/appeals/create">
              <Button>Создать первое обращение</Button>
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {data?.items.map((appeal) => (
              <div key={appeal.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {appeal.title}
                    </h3>
                    <p className="text-gray-600 mb-2">{appeal.description}</p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      appeal.status === AppealStatus.RESOLVED
                        ? 'bg-green-100 text-green-800'
                        : appeal.status === AppealStatus.IN_PROGRESS
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {statusLabels[appeal.status]}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 text-sm text-gray-600">
                  <span className="px-2 py-1 bg-gray-100 rounded">
                    {categoryLabels[appeal.category]}
                  </span>
                  {appeal.district && (
                    <span className="px-2 py-1 bg-gray-100 rounded">
                      {appeal.district}
                    </span>
                  )}
                  <span className="px-2 py-1 bg-gray-100 rounded">
                    {new Date(appeal.created_at).toLocaleDateString('ru-RU')}
                  </span>
                </div>
                {appeal.ai_summary && (
                  <div className="mt-4 p-3 bg-blue-50 rounded">
                    <p className="text-sm text-gray-700">
                      <strong>AI резюме:</strong> {appeal.ai_summary}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

