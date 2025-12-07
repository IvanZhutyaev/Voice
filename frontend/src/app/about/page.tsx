import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">Г</span>
            </div>
            <span className="text-2xl font-bold text-gray-900">Глас</span>
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">О проекте Глас</h1>

        <div className="prose prose-lg max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Миссия проекта</h2>
            <p className="text-gray-700 mb-4">
              <strong>Глас</strong> — это интеллектуальная мультиплатформенная система для сбора, анализа и управления обращениями граждан.
              Система использует искусственный интеллект для понимания текстов, фото и голосовых сообщений, автоматически маршрутизирует их
              по ответственным отделам городской администрации и визуализирует результаты.
            </p>
            <p className="text-gray-700">
              Главная цель — сделать взаимодействие между жителями и властью прозрачным, быстрым и эффективным.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Наши ценности</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li><strong>Прозрачность:</strong> каждый житель видит, что его обращение не пропало, а действительно рассматривается и решается</li>
              <li><strong>Доступность:</strong> простой интерфейс для любого возраста и уровня цифровой грамотности</li>
              <li><strong>Этичный ИИ:</strong> никакой слежки, только помощь и аналитика, направленные на благо города</li>
              <li><strong>Эффективность:</strong> городские службы получают структурированные данные, аналитические отчёты и приоритеты проблем</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Возможности системы</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold mb-2">Для граждан</h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700">
                  <li>Создание обращений (текст, фото, голос)</li>
                  <li>Отслеживание статуса обращения</li>
                  <li>Геолокация проблем на карте</li>
                  <li>Уведомления о статусе</li>
                  <li>Оценка качества решения</li>
                </ul>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold mb-2">Для администраторов</h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700">
                  <li>Дашборд с аналитикой</li>
                  <li>Управление обращениями</li>
                  <li>Автоматическая классификация</li>
                  <li>Экспорт отчетов</li>
                  <li>Тепловые карты проблем</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Технологии</h2>
            <p className="text-gray-700 mb-4">
              Проект построен на современных технологиях:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li><strong>Frontend:</strong> Next.js, React, TypeScript, TailwindCSS</li>
              <li><strong>Backend:</strong> FastAPI, PostgreSQL, Redis</li>
              <li><strong>AI/NLP:</strong> OpenAI API, spaCy, Transformers</li>
              <li><strong>Инфраструктура:</strong> Docker, Kubernetes</li>
            </ul>
          </section>

          <div className="mt-8">
            <Link href="/register">
              <Button size="lg">Начать использовать</Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

