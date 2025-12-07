import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">Г</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">Глас</span>
          </div>
          <nav className="flex space-x-4">
            <Link href="/login" className="text-gray-600 hover:text-gray-900">
              Вход
            </Link>
            <Link href="/register">
              <Button>Регистрация</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Глас — голос города
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Умный гражданский ИИ-ассистент для сбора, анализа и управления обращениями граждан.
          Сделайте свой город лучше вместе с нами.
        </p>
        <div className="flex justify-center space-x-4">
          <Link href="/register">
            <Button size="lg">Создать обращение</Button>
          </Link>
          <Link href="/about">
            <Button size="lg" variant="outline">Узнать больше</Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🤖</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Искусственный интеллект</h3>
            <p className="text-gray-600">
              Автоматическая классификация и анализ обращений с помощью AI
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📍</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Геолокация</h3>
            <p className="text-gray-600">
              Точное определение местоположения проблем на карте города
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Аналитика</h3>
            <p className="text-gray-600">
              Детальная статистика и визуализация данных для управленцев
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-20">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 Глас. Все права защищены.</p>
        </div>
      </footer>
    </main>
  )
}

