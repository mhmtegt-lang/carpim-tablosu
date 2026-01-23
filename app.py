import React, { useState, useEffect } from 'react';
import { Check, X, RotateCcw, Award, BookOpen, ClipboardCheck } from 'lucide-react';

const CarpimTablosuApp = () => {
  const [mode, setMode] = useState('menu'); // menu, ogretim, degerlendirme
  const [zorlukSeviyesi, setZorlukSeviyesi] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [isAnswerVisible, setIsAnswerVisible] = useState(true);
  const [isCovered, setIsCovered] = useState(false);
  const [showCheck, setShowCheck] = useState(false);
  const [isCorrect, setIsCorrect] = useState(null);
  const [score, setScore] = useState(0);
  const [completedProblems, setCompletedProblems] = useState([]);
  const [degerlendirmeAnswers, setDegerlendirmeAnswers] = useState({});
  const [degerlendirmeComplete, setDegerlendirmeComplete] = useState(false);

  // Zorluk seviyelerine göre çarpma işlemleri
  const problemSets = {
    kolay: [
      { sayi1: 2, sayi2: 3 }, { sayi1: 2, sayi2: 4 }, { sayi1: 2, sayi2: 5 },
      { sayi1: 3, sayi2: 3 }, { sayi1: 3, sayi2: 4 }, { sayi1: 3, sayi2: 5 },
      { sayi1: 4, sayi2: 4 }, { sayi1: 4, sayi2: 5 }, { sayi1: 5, sayi2: 5 }
    ],
    orta: [
      { sayi1: 2, sayi2: 6 }, { sayi1: 2, sayi2: 7 }, { sayi1: 2, sayi2: 8 }, { sayi1: 2, sayi2: 9 },
      { sayi1: 3, sayi2: 6 }, { sayi1: 3, sayi2: 7 }, { sayi1: 3, sayi2: 8 }, { sayi1: 3, sayi2: 9 },
      { sayi1: 4, sayi2: 6 }, { sayi1: 4, sayi2: 7 }, { sayi1: 4, sayi2: 8 }, { sayi1: 4, sayi2: 9 },
      { sayi1: 5, sayi2: 6 }, { sayi1: 5, sayi2: 7 }, { sayi1: 5, sayi2: 8 }, { sayi1: 5, sayi2: 9 }
    ],
    zor: [
      { sayi1: 6, sayi2: 6 }, { sayi1: 6, sayi2: 7 }, { sayi1: 6, sayi2: 8 }, { sayi1: 6, sayi2: 9 },
      { sayi1: 7, sayi2: 7 }, { sayi1: 7, sayi2: 8 }, { sayi1: 7, sayi2: 9 },
      { sayi1: 8, sayi2: 8 }, { sayi1: 8, sayi2: 9 },
      { sayi1: 9, sayi2: 9 }
    ]
  };

  const getCurrentProblems = () => {
    if (!zorlukSeviyesi) return [];
    return problemSets[zorlukSeviyesi];
  };

  const currentProblem = getCurrentProblems()[currentIndex];

  const handleCover = () => {
    setIsCovered(true);
    setIsAnswerVisible(false);
    setUserAnswer('');
    setShowCheck(false);
    setIsCorrect(null);
  };

  const handleUncover = () => {
    const correct = parseInt(userAnswer) === (currentProblem.sayi1 * currentProblem.sayi2);
    setIsCorrect(correct);
    setIsCovered(false);
    setIsAnswerVisible(true);
    setShowCheck(true);
    
    if (correct) {
      setScore(score + 1);
      setCompletedProblems([...completedProblems, currentIndex]);
    }
  };

  const handleNext = () => {
    if (currentIndex < getCurrentProblems().length - 1) {
      setCurrentIndex(currentIndex + 1);
      setUserAnswer('');
      setIsAnswerVisible(true);
      setIsCovered(false);
      setShowCheck(false);
      setIsCorrect(null);
    } else {
      alert(`Tebrikler! ${score + (isCorrect ? 1 : 0)}/${getCurrentProblems().length} doğru yaptınız!`);
    }
  };

  const handleRetry = () => {
    setUserAnswer('');
    setIsAnswerVisible(true);
    setIsCovered(false);
    setShowCheck(false);
    setIsCorrect(null);
  };

  const resetOgretim = () => {
    setCurrentIndex(0);
    setUserAnswer('');
    setIsAnswerVisible(true);
    setIsCovered(false);
    setShowCheck(false);
    setIsCorrect(null);
    setScore(0);
    setCompletedProblems([]);
  };

  // Değerlendirme işlemleri - karışık 20 soru
  const degerlendirmeProblemleri = [
    { sayi1: 3, sayi2: 4 }, { sayi1: 7, sayi2: 8 }, { sayi1: 2, sayi2: 6 }, { sayi1: 9, sayi2: 9 },
    { sayi1: 4, sayi2: 5 }, { sayi1: 6, sayi2: 7 }, { sayi1: 3, sayi2: 8 }, { sayi1: 5, sayi2: 5 },
    { sayi1: 8, sayi2: 9 }, { sayi1: 2, sayi2: 7 }, { sayi1: 6, sayi2: 6 }, { sayi1: 4, sayi2: 9 },
    { sayi1: 3, sayi2: 7 }, { sayi1: 5, sayi2: 8 }, { sayi1: 7, sayi2: 7 }, { sayi1: 2, sayi2: 9 },
    { sayi1: 6, sayi2: 8 }, { sayi1: 4, sayi2: 7 }, { sayi1: 8, sayi2: 8 }, { sayi1: 5, sayi2: 9 }
  ];

  const handleDegerlendirmeSubmit = () => {
    let correctCount = 0;
    degerlendirmeProblemleri.forEach((problem, index) => {
      const userAns = parseInt(degerlendirmeAnswers[index]);
      if (userAns === problem.sayi1 * problem.sayi2) {
        correctCount++;
      }
    });
    setScore(correctCount);
    setDegerlendirmeComplete(true);
  };

  const resetDegerlendirme = () => {
    setDegerlendirmeAnswers({});
    setDegerlendirmeComplete(false);
    setScore(0);
  };

  if (mode === 'menu') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
            <h1 className="text-4xl font-bold text-center text-indigo-800 mb-4">
              Kapat-Kopyala-Karşılaştır
            </h1>
            <h2 className="text-2xl text-center text-indigo-600 mb-8">
              Çarpım Tablosu Öğretimi
            </h2>
            
            <div className="bg-indigo-50 rounded-lg p-6 mb-8">
              <h3 className="font-semibold text-lg mb-3 text-indigo-900">Nasıl Çalışır?</h3>
              <ol className="space-y-2 text-gray-700">
                <li><span className="font-semibold">1. Oku:</span> İşlemi ve cevabını oku</li>
                <li><span className="font-semibold">2. Kapat:</span> İşlemi kapat</li>
                <li><span className="font-semibold">3. Yaz:</span> İşlemi ezberden yaz</li>
                <li><span className="font-semibold">4. Karşılaştır:</span> Cevabını kontrol et</li>
              </ol>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <button
                onClick={() => setMode('ogretim')}
                className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl p-8 hover:from-green-600 hover:to-green-700 transition transform hover:scale-105 shadow-lg"
              >
                <BookOpen className="w-16 h-16 mx-auto mb-4" />
                <h3 className="text-2xl font-bold mb-2">Öğretim Modu</h3>
                <p className="text-green-100">Çarpım tablosunu adım adım öğren</p>
              </button>

              <button
                onClick={() => setMode('degerlendirme')}
                className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-xl p-8 hover:from-purple-600 hover:to-purple-700 transition transform hover:scale-105 shadow-lg"
              >
                <ClipboardCheck className="w-16 h-16 mx-auto mb-4" />
                <h3 className="text-2xl font-bold mb-2">Değerlendirme</h3>
                <p className="text-purple-100">Öğrendiklerini test et (20 soru)</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (mode === 'ogretim') {
    if (!zorlukSeviyesi) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-3xl mx-auto">
            <button
              onClick={() => setMode('menu')}
              className="mb-6 px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
            >
              ← Ana Menü
            </button>
            
            <div className="bg-white rounded-2xl shadow-2xl p-8">
              <h2 className="text-3xl font-bold text-center text-indigo-800 mb-8">
                Zorluk Seviyesi Seç
              </h2>
              
              <div className="space-y-4">
                <button
                  onClick={() => setZorlukSeviyesi('kolay')}
                  className="w-full bg-green-500 text-white rounded-xl p-6 hover:bg-green-600 transition shadow-lg"
                >
                  <h3 className="text-2xl font-bold mb-2">Kolay</h3>
                  <p className="text-green-100">2, 3, 4, 5 sayılarının birbirleriyle çarpımı</p>
                </button>

                <button
                  onClick={() => setZorlukSeviyesi('orta')}
                  className="w-full bg-yellow-500 text-white rounded-xl p-6 hover:bg-yellow-600 transition shadow-lg"
                >
                  <h3 className="text-2xl font-bold mb-2">Orta</h3>
                  <p className="text-yellow-100">2, 3, 4, 5 sayılarının 6, 7, 8, 9 ile çarpımı</p>
                </button>

                <button
                  onClick={() => setZorlukSeviyesi('zor')}
                  className="w-full bg-red-500 text-white rounded-xl p-6 hover:bg-red-600 transition shadow-lg"
                >
                  <h3 className="text-2xl font-bold mb-2">Zor</h3>
                  <p className="text-red-100">6, 7, 8, 9 sayılarının birbirleriyle çarpımı</p>
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <button
              onClick={() => {
                setZorlukSeviyesi(null);
                resetOgretim();
              }}
              className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
            >
              ← Geri
            </button>
            <div className="text-lg font-semibold text-indigo-800">
              Soru {currentIndex + 1} / {getCurrentProblems().length}
            </div>
            <div className="text-lg font-semibold text-green-600">
              Puan: {score}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <div className="grid grid-cols-3 gap-6 mb-8">
              {/* Sütun 1: İşlem ve Cevap */}
              <div className={`relative border-2 border-indigo-300 rounded-lg p-8 bg-indigo-50 transition-all duration-500 min-h-[200px] flex items-center justify-center ${isCovered ? 'scale-95' : 'scale-100'}`}>
                <div className={`text-center transition-all duration-500 transform ${isCovered ? 'rotate-y-90 opacity-0' : 'rotate-y-0 opacity-100'}`}>
                  <div className="text-2xl font-bold text-indigo-800 whitespace-nowrap">
                    {currentProblem.sayi1} × {currentProblem.sayi2}{isAnswerVisible && <span className="text-green-600"> = {currentProblem.sayi1 * currentProblem.sayi2}</span>}
                  </div>
                </div>
                {isCovered && (
                  <div className="absolute inset-0 bg-gradient-to-br from-gray-300 to-gray-400 rounded-lg flex items-center justify-center transform transition-all duration-500 shadow-xl">
                    <div className="text-gray-600 font-semibold text-lg rotate-[-5deg]">
                      Kapalı
                    </div>
                  </div>
                )}
              </div>

              {/* Sütun 2: Öğrenci Cevabı */}
              <div className="border-2 border-blue-300 rounded-lg p-8 bg-blue-50 min-h-[200px] flex items-center justify-center">
                <div className="text-center w-full">
                  <div className="text-2xl font-bold text-blue-800 flex items-center justify-center gap-2">
                    <span className="whitespace-nowrap">{currentProblem.sayi1} × {currentProblem.sayi2} =</span>
                    <input
                      type="number"
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      disabled={!isCovered}
                      className="w-20 text-2xl font-bold text-center border-2 border-blue-400 rounded-lg p-2 disabled:bg-gray-100 disabled:cursor-not-allowed"
                      placeholder="?"
                    />
                  </div>
                </div>
              </div>

              {/* Sütun 3: Kontrol */}
              <div className="border-2 border-purple-300 rounded-lg p-8 bg-purple-50 flex items-center justify-center min-h-[200px]">
                {showCheck && (
                  <div className="text-center animate-bounce">
                    {isCorrect ? (
                      <Check className="w-20 h-20 text-green-500 mx-auto" />
                    ) : (
                      <X className="w-20 h-20 text-red-500 mx-auto" />
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-4">
              {!isCovered && !showCheck && (
                <button
                  onClick={handleCover}
                  className="w-full bg-indigo-600 text-white rounded-lg py-4 text-xl font-semibold hover:bg-indigo-700 transition"
                >
                  2. Kapat
                </button>
              )}

              {isCovered && !showCheck && (
                <button
                  onClick={handleUncover}
                  disabled={!userAnswer}
                  className="w-full bg-green-600 text-white rounded-lg py-4 text-xl font-semibold hover:bg-green-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  4. Karşılaştır
                </button>
              )}

              {showCheck && (
                <div className="flex gap-4">
                  {isCorrect ? (
                    <button
                      onClick={handleNext}
                      className="flex-1 bg-green-600 text-white rounded-lg py-4 text-xl font-semibold hover:bg-green-700 transition"
                    >
                      {currentIndex < getCurrentProblems().length - 1 ? 'Sonraki Soru →' : 'Tamamla'}
                    </button>
                  ) : (
                    <button
                      onClick={handleRetry}
                      className="flex-1 bg-orange-600 text-white rounded-lg py-4 text-xl font-semibold hover:bg-orange-700 transition flex items-center justify-center gap-2"
                    >
                      <RotateCcw className="w-6 h-6" />
                      Tekrar Dene
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (mode === 'degerlendirme') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
        <div className="max-w-5xl mx-auto">
          <button
            onClick={() => {
              setMode('menu');
              resetDegerlendirme();
            }}
            className="mb-6 px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
          >
            ← Ana Menü
          </button>

          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <h2 className="text-3xl font-bold text-center text-purple-800 mb-8">
              Değerlendirme Testi
            </h2>

            {!degerlendirmeComplete ? (
              <>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  {degerlendirmeProblemleri.map((problem, index) => (
                    <div key={index} className="border-2 border-purple-300 rounded-lg p-4 bg-purple-50">
                      <div className="text-center mb-2">
                        <span className="text-sm font-semibold text-purple-600">Soru {index + 1}</span>
                      </div>
                      <div className="text-xl font-bold text-purple-800 text-center mb-2">
                        {problem.sayi1} × {problem.sayi2} =
                      </div>
                      <input
                        type="number"
                        value={degerlendirmeAnswers[index] || ''}
                        onChange={(e) => setDegerlendirmeAnswers({
                          ...degerlendirmeAnswers,
                          [index]: e.target.value
                        })}
                        className="w-full text-center text-lg font-bold border-2 border-purple-300 rounded-lg p-2"
                        placeholder="?"
                      />
                    </div>
                  ))}
                </div>

                <button
                  onClick={handleDegerlendirmeSubmit}
                  disabled={Object.keys(degerlendirmeAnswers).length < degerlendirmeProblemleri.length}
                  className="w-full bg-purple-600 text-white rounded-lg py-4 text-xl font-semibold hover:bg-purple-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  Testi Tamamla
                </button>
              </>
            ) : (
              <div className="text-center">
                <Award className="w-24 h-24 text-yellow-500 mx-auto mb-6" />
                <h3 className="text-4xl font-bold text-purple-800 mb-4">
                  Test Tamamlandı!
                </h3>
                <div className="text-6xl font-bold text-green-600 mb-8">
                  {score} / {degerlendirmeProblemleri.length}
                </div>
                <div className="text-2xl text-gray-700 mb-8">
                  Başarı Oranı: {Math.round((score / degerlendirmeProblemleri.length) * 100)}%
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  {degerlendirmeProblemleri.map((problem, index) => {
                    const userAns = parseInt(degerlendirmeAnswers[index]);
                    const correctAns = problem.sayi1 * problem.sayi2;
                    const isCorrect = userAns === correctAns;

                    return (
                      <div
                        key={index}
                        className={`border-2 rounded-lg p-4 ${
                          isCorrect ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'
                        }`}
                      >
                        <div className="text-center mb-2">
                          <span className="text-sm font-semibold">Soru {index + 1}</span>
                        </div>
                        <div className="text-lg font-bold text-center mb-1">
                          {problem.sayi1} × {problem.sayi2}
                        </div>
                        <div className="text-center">
                          <div className={`font-bold ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                            Senin: {userAns || '-'}
                          </div>
                          {!isCorrect && (
                            <div className="text-green-600 font-bold">
                              Doğru: {correctAns}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

                <button
                  onClick={resetDegerlendirme}
                  className="bg-purple-600 text-white rounded-lg py-4 px-8 text-xl font-semibold hover:bg-purple-700 transition"
                >
                  Tekrar Dene
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }
};

export default CarpimTablosuApp;  bu kod olur mu
