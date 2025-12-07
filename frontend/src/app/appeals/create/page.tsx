'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { api } from '@/lib/api'
import { AppealCreate, AppealCategory } from '@/lib/types'
import { Button } from '@/components/ui/button'

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

export default function CreateAppealPage() {
  const router = useRouter()
  const { register, handleSubmit, formState: { errors } } = useForm<AppealCreate>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (data: AppealCreate) => {
    setError('')
    setLoading(true)

    try {
      await api.post('/appeals', data)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка создания обращения')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Создать обращение</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-lg shadow p-6 space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Заголовок *
            </label>
            <input
              id="title"
              {...register('title', { required: true, minLength: 5 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            {errors.title && (
              <p className="text-red-600 text-sm mt-1">Заголовок должен быть не менее 5 символов</p>
            )}
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Описание проблемы *
            </label>
            <textarea
              id="description"
              {...register('description', { required: true, minLength: 10 })}
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            {errors.description && (
              <p className="text-red-600 text-sm mt-1">Описание должно быть не менее 10 символов</p>
            )}
          </div>

          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Категория (необязательно, будет определена автоматически)
            </label>
            <select
              id="category"
              {...register('category')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Автоматически</option>
              {Object.entries(categoryLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="latitude" className="block text-sm font-medium text-gray-700 mb-1">
                Широта (необязательно)
              </label>
              <input
                id="latitude"
                type="number"
                step="any"
                {...register('latitude', { valueAsNumber: true })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label htmlFor="longitude" className="block text-sm font-medium text-gray-700 mb-1">
                Долгота (необязательно)
              </label>
              <input
                id="longitude"
                type="number"
                step="any"
                {...register('longitude', { valueAsNumber: true })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div>
            <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
              Адрес (необязательно)
            </label>
            <input
              id="address"
              {...register('address')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="flex space-x-4">
            <Button type="submit" disabled={loading}>
              {loading ? 'Создание...' : 'Создать обращение'}
            </Button>
            <Button type="button" variant="outline" onClick={() => router.back()}>
              Отмена
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

