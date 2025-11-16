"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, AlertTriangle, CheckCircle2, Shield, TrendingUp, Loader2, Sparkles, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from './ui/button';

interface AnalysisData {
  analysis_id: string;
  graph_id: string;
  execution_id: string;
  team_id?: string;
  model?: string;
  summary: string;
  vulnerabilities: string[];
  security_issues: string[];
  recommendations: string[];
  detailed_analysis: string;
  risk_score: number | null;
  generated_at: string;
}

interface AnalysisPanelProps {
  isOpen: boolean;
  onClose: () => void;
  graphId: string | null;
  executionId: string | null;
  onAnalysisGenerated?: (analysis: AnalysisData) => void;
}

export default function AnalysisPanel({
  isOpen,
  onClose,
  graphId,
  executionId,
  onAnalysisGenerated
}: AnalysisPanelProps) {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDetailedAnalysis, setShowDetailedAnalysis] = useState(false);

  const fetchAnalysis = async () => {
    if (!graphId || !executionId) {
      setError('Missing graph ID or execution ID');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/analysis/llm-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          graph_id: graphId,
          execution_id: executionId,
          focus_areas: ['security', 'vulnerabilities', 'prompt_injection']
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || 'Failed to generate analysis');
      }

      const data = await response.json();
      setAnalysisData(data);
      
      if (onAnalysisGenerated) {
        onAnalysisGenerated(data);
      }
    } catch (err) {
      console.error('Failed to fetch analysis:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-fetch when panel opens with valid IDs
  useEffect(() => {
    if (isOpen && graphId && executionId && !analysisData) {
      fetchAnalysis();
    }
  }, [isOpen, graphId, executionId]);

  const getRiskColor = (score: number | null) => {
    if (score === null) return 'text-zinc-500';
    if (score >= 75) return 'text-red-600';
    if (score >= 50) return 'text-orange-600';
    if (score >= 25) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getRiskBgColor = (score: number | null) => {
    if (score === null) return 'bg-zinc-200';
    if (score >= 75) return 'bg-red-100';
    if (score >= 50) return 'bg-orange-100';
    if (score >= 25) return 'bg-yellow-100';
    return 'bg-green-100';
  };

  const getRiskLabel = (score: number | null) => {
    if (score === null) return 'Unknown';
    if (score >= 75) return 'Critical';
    if (score >= 50) return 'High';
    if (score >= 25) return 'Medium';
    return 'Low';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/30 backdrop-blur-sm z-[100]"
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 30, stiffness: 300 }}
            className="fixed right-0 top-0 h-full w-full max-w-2xl bg-white dark:bg-zinc-900 shadow-2xl z-[101] overflow-hidden flex flex-col"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-200 dark:border-zinc-800 bg-gradient-to-r from-violet-50 to-purple-50 dark:from-violet-950/20 dark:to-purple-950/20">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-50">
                    AI Security Analysis
                  </h2>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400">
                    {analysisData?.team_id ? `Team: ${analysisData.team_id}` : 'LLM-powered execution insights'}
                  </p>
                </div>
              </div>
              <Button
                onClick={onClose}
                size="icon"
                variant="ghost"
                className="hover:bg-zinc-200 dark:hover:bg-zinc-800"
              >
                <X className="w-5 h-5" />
              </Button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex flex-col items-center justify-center h-full gap-4"
                >
                  <Loader2 className="w-12 h-12 text-violet-600 animate-spin" />
                  <div className="text-center">
                    <p className="text-lg font-semibold text-zinc-900 dark:text-zinc-50 mb-1">
                      Analyzing Execution...
                    </p>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">
                      AI is reviewing your graph execution for security issues
                    </p>
                  </div>
                </motion.div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-xl p-4 flex items-start gap-3"
                >
                  <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5" />
                  <div>
                    <p className="font-semibold text-red-900 dark:text-red-200">Error</p>
                    <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                    <Button
                      onClick={fetchAnalysis}
                      size="sm"
                      className="mt-3 bg-red-600 hover:bg-red-700"
                    >
                      Retry Analysis
                    </Button>
                  </div>
                </motion.div>
              )}

              {!isLoading && !error && !analysisData && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex flex-col items-center justify-center h-full gap-4 text-center"
                >
                  <div className="p-4 bg-violet-100 dark:bg-violet-950/30 rounded-2xl">
                    <Sparkles className="w-12 h-12 text-violet-600 dark:text-violet-400" />
                  </div>
                  <div>
                    <p className="text-lg font-semibold text-zinc-900 dark:text-zinc-50 mb-2">
                      No Analysis Available
                    </p>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
                      Run the graph to generate an AI-powered security analysis
                    </p>
                    {graphId && executionId && (
                      <Button
                        onClick={fetchAnalysis}
                        className="bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
                      >
                        <Sparkles className="w-4 h-4 mr-2" />
                        Generate Analysis
                      </Button>
                    )}
                  </div>
                </motion.div>
              )}

              {!isLoading && !error && analysisData && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  {/* Metadata */}
                  <div className="bg-blue-50 dark:bg-blue-950/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800">
                    <div className="flex flex-col gap-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-zinc-600 dark:text-zinc-400">Analysis ID:</span>
                        <span className="font-mono text-zinc-900 dark:text-zinc-50 text-xs">{analysisData.analysis_id.slice(0, 8)}</span>
                      </div>
                      {analysisData.team_id && (
                        <div className="flex justify-between">
                          <span className="text-zinc-600 dark:text-zinc-400">Team ID:</span>
                          <span className="font-mono text-zinc-900 dark:text-zinc-50 text-xs">{analysisData.team_id}</span>
                        </div>
                      )}
                      {analysisData.model && (
                        <div className="flex justify-between">
                          <span className="text-zinc-600 dark:text-zinc-400">Model:</span>
                          <span className="font-mono text-zinc-900 dark:text-zinc-50 text-xs">{analysisData.model.split('.').pop()}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Risk Score */}
                  <div className={`rounded-xl p-5 ${getRiskBgColor(analysisData.risk_score)} border-2 ${analysisData.risk_score && analysisData.risk_score >= 50 ? 'border-red-300 dark:border-red-800' : 'border-green-300 dark:border-green-800'}`}>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <Shield className={`w-5 h-5 ${getRiskColor(analysisData.risk_score)}`} />
                        <span className="font-semibold text-zinc-900 dark:text-zinc-50">
                          Risk Assessment
                        </span>
                      </div>
                      <span className={`text-2xl font-bold ${getRiskColor(analysisData.risk_score)}`}>
                        {analysisData.risk_score ?? 'N/A'}
                        {analysisData.risk_score !== null && '/100'}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-white dark:bg-zinc-800 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${analysisData.risk_score ?? 0}%` }}
                          transition={{ duration: 1, ease: 'easeOut' }}
                          className={`h-full ${analysisData.risk_score && analysisData.risk_score >= 50 ? 'bg-gradient-to-r from-orange-500 to-red-600' : 'bg-gradient-to-r from-green-500 to-emerald-600'}`}
                        />
                      </div>
                      <span className={`text-sm font-semibold ${getRiskColor(analysisData.risk_score)}`}>
                        {getRiskLabel(analysisData.risk_score)}
                      </span>
                    </div>
                  </div>

                  {/* Summary */}
                  <div className="bg-zinc-50 dark:bg-zinc-800/50 rounded-xl p-5 border border-zinc-200 dark:border-zinc-700">
                    <div className="flex items-center gap-2 mb-3">
                      <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">Summary</h3>
                    </div>
                    <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">
                      {analysisData.summary}
                    </p>
                  </div>

                  {/* Vulnerabilities */}
                  {analysisData.vulnerabilities.length > 0 && (
                    <div className="bg-red-50 dark:bg-red-950/20 rounded-xl p-5 border border-red-200 dark:border-red-800">
                      <div className="flex items-center gap-2 mb-3">
                        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
                        <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">
                          Vulnerabilities Detected ({analysisData.vulnerabilities.length})
                        </h3>
                      </div>
                      <ul className="space-y-2">
                        {analysisData.vulnerabilities.map((vuln, idx) => (
                          <motion.li
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="flex items-start gap-2 text-zinc-700 dark:text-zinc-300"
                          >
                            <span className="text-red-600 dark:text-red-400 mt-1">•</span>
                            <span>{vuln}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Security Issues */}
                  {analysisData.security_issues.length > 0 && (
                    <div className="bg-orange-50 dark:bg-orange-950/20 rounded-xl p-5 border border-orange-200 dark:border-orange-800">
                      <div className="flex items-center gap-2 mb-3">
                        <Shield className="w-5 h-5 text-orange-600 dark:text-orange-400" />
                        <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">
                          Security Concerns ({analysisData.security_issues.length})
                        </h3>
                      </div>
                      <ul className="space-y-2">
                        {analysisData.security_issues.map((issue, idx) => (
                          <motion.li
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="flex items-start gap-2 text-zinc-700 dark:text-zinc-300"
                          >
                            <span className="text-orange-600 dark:text-orange-400 mt-1">•</span>
                            <span>{issue}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Recommendations */}
                  {analysisData.recommendations.length > 0 && (
                    <div className="bg-green-50 dark:bg-green-950/20 rounded-xl p-5 border border-green-200 dark:border-green-800">
                      <div className="flex items-center gap-2 mb-3">
                        <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
                        <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">
                          Recommendations ({analysisData.recommendations.length})
                        </h3>
                      </div>
                      <ul className="space-y-2">
                        {analysisData.recommendations.map((rec, idx) => (
                          <motion.li
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="flex items-start gap-2 text-zinc-700 dark:text-zinc-300"
                          >
                            <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                            <span>{rec}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Detailed Analysis (Collapsible) */}
                  <div className="bg-zinc-50 dark:bg-zinc-800/50 rounded-xl border border-zinc-200 dark:border-zinc-700 overflow-hidden">
                    <button
                      onClick={() => setShowDetailedAnalysis(!showDetailedAnalysis)}
                      className="w-full flex items-center justify-between p-5 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                    >
                      <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">
                        Detailed Analysis
                      </h3>
                      {showDetailedAnalysis ? (
                        <ChevronUp className="w-5 h-5 text-zinc-500" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-zinc-500" />
                      )}
                    </button>
                    <AnimatePresence>
                      {showDetailedAnalysis && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="border-t border-zinc-200 dark:border-zinc-700"
                        >
                          <div className="p-5">
                            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed whitespace-pre-wrap">
                              {analysisData.detailed_analysis}
                            </p>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* Regenerate Button */}
                  <div className="flex justify-center pt-4">
                    <Button
                      onClick={fetchAnalysis}
                      variant="outline"
                      className="border-violet-300 dark:border-violet-700 text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-950/30"
                    >
                      <Sparkles className="w-4 h-4 mr-2" />
                      Regenerate Analysis
                    </Button>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

