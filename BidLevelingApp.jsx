import React, { useState } from 'react';

const API_URL = 'http://localhost:5000/api';

export default function BidLevelingApp() {
  const [files, setFiles] = useState([]);
  const [bidderNames, setBidderNames] = useState([]);
  const [analyses, setAnalyses] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('single'); // 'single' or 'compare'

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    setBidderNames(selectedFiles.map((f, i) => `Bidder ${i + 1}`));
    setAnalyses(null);
    setError(null);
  };

  const updateBidderName = (index, name) => {
    const newNames = [...bidderNames];
    newNames[index] = name;
    setBidderNames(newNames);
  };

  const analyzeBids = async () => {
    if (files.length === 0) {
      setError('Please select at least one PDF file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (mode === 'single' && files.length === 1) {
        // Single bid analysis
        const formData = new FormData();
        formData.append('file', files[0]);
        formData.append('bidder_name', bidderNames[0]);

        const response = await fetch(`${API_URL}/analyze-bid`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Analysis failed');
        }

        const data = await response.json();
        setAnalyses({ individual_analyses: [data] });
      } else {
        // Multiple bids comparison
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        bidderNames.forEach(name => formData.append('bidder_names', name));

        const response = await fetch(`${API_URL}/compare-bids`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Comparison failed');
        }

        const data = await response.json();
        setAnalyses(data);
      }
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationColor = (rec) => {
    if (rec === 'RECOMMEND') return '#00ff88';
    if (rec === 'RECOMMEND WITH CAUTION') return '#ffaa00';
    return '#ff4444';
  };

  const getRiskColor = (risk) => {
    if (risk === 'LOW') return '#00ff88';
    if (risk === 'MEDIUM') return '#ffaa00';
    return '#ff4444';
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0a0e1a',
      backgroundImage: `
        linear-gradient(rgba(0, 100, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 100, 255, 0.03) 1px, transparent 1px)
      `,
      backgroundSize: '40px 40px',
      color: '#e0e6ed',
      fontFamily: '"JetBrains Mono", "Courier New", monospace',
      padding: '0',
      margin: '0',
    }}>
      {/* Header */}
      <div style={{
        borderBottom: '2px solid #1a4d8f',
        background: 'linear-gradient(180deg, #0f1624 0%, #0a0e1a 100%)',
        padding: '2rem 3rem',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.05,
          backgroundImage: `repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            #0064ff 10px,
            #0064ff 11px
          )`,
        }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div style={{
            fontSize: '0.75rem',
            color: '#4a8fe7',
            letterSpacing: '0.15em',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
          }}>
            CONSTRUCTION INTELLIGENCE SYSTEM
          </div>
          <h1 style={{
            margin: 0,
            fontSize: '2.5rem',
            fontWeight: 700,
            background: 'linear-gradient(135deg, #4a8fe7 0%, #00d4ff 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.02em',
          }}>
            BID LEVELING AI
          </h1>
          <div style={{
            marginTop: '0.75rem',
            fontSize: '0.9rem',
            color: '#6b8cae',
            letterSpacing: '0.05em',
          }}>
            Powered by Claude AI • Advanced Procurement Analysis
          </div>
        </div>
      </div>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '3rem' }}>
        {/* Upload Section */}
        <div style={{
          background: 'rgba(15, 22, 36, 0.6)',
          border: '1px solid #1a4d8f',
          borderRadius: '8px',
          padding: '2rem',
          marginBottom: '2rem',
          backdropFilter: 'blur(10px)',
        }}>
          <div style={{
            display: 'flex',
            gap: '1rem',
            marginBottom: '1.5rem',
          }}>
            <button
              onClick={() => setMode('single')}
              style={{
                padding: '0.75rem 1.5rem',
                background: mode === 'single' ? '#1a4d8f' : 'transparent',
                border: '1px solid #1a4d8f',
                color: mode === 'single' ? '#00d4ff' : '#6b8cae',
                borderRadius: '4px',
                cursor: 'pointer',
                fontFamily: 'inherit',
                fontSize: '0.9rem',
                letterSpacing: '0.05em',
                transition: 'all 0.2s',
              }}
            >
              SINGLE BID ANALYSIS
            </button>
            <button
              onClick={() => setMode('compare')}
              style={{
                padding: '0.75rem 1.5rem',
                background: mode === 'compare' ? '#1a4d8f' : 'transparent',
                border: '1px solid #1a4d8f',
                color: mode === 'compare' ? '#00d4ff' : '#6b8cae',
                borderRadius: '4px',
                cursor: 'pointer',
                fontFamily: 'inherit',
                fontSize: '0.9rem',
                letterSpacing: '0.05em',
                transition: 'all 0.2s',
              }}
            >
              COMPARE MULTIPLE BIDS
            </button>
          </div>

          <div style={{
            border: '2px dashed #1a4d8f',
            borderRadius: '6px',
            padding: '2rem',
            textAlign: 'center',
            background: 'rgba(0, 100, 255, 0.02)',
            marginBottom: '1.5rem',
          }}>
            <input
              type="file"
              multiple={mode === 'compare'}
              accept=".pdf"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" style={{
              cursor: 'pointer',
              display: 'inline-block',
            }}>
              <div style={{
                fontSize: '3rem',
                marginBottom: '1rem',
                color: '#4a8fe7',
              }}>
                📄
              </div>
              <div style={{
                fontSize: '1.1rem',
                color: '#e0e6ed',
                marginBottom: '0.5rem',
              }}>
                {files.length > 0 ? `${files.length} file(s) selected` : 'Click to upload PDF bid documents'}
              </div>
              <div style={{
                fontSize: '0.85rem',
                color: '#6b8cae',
              }}>
                {mode === 'compare' ? 'Upload 2+ PDFs to compare' : 'Upload a single PDF for analysis'}
              </div>
            </label>
          </div>

          {files.length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              {files.map((file, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem',
                  padding: '0.75rem',
                  background: 'rgba(26, 77, 143, 0.1)',
                  border: '1px solid #1a4d8f',
                  borderRadius: '4px',
                  marginBottom: '0.5rem',
                }}>
                  <div style={{ flex: 1, fontSize: '0.9rem' }}>
                    📎 {file.name}
                  </div>
                  <input
                    type="text"
                    value={bidderNames[index]}
                    onChange={(e) => updateBidderName(index, e.target.value)}
                    placeholder="Bidder name"
                    style={{
                      padding: '0.5rem',
                      background: '#0f1624',
                      border: '1px solid #1a4d8f',
                      borderRadius: '4px',
                      color: '#e0e6ed',
                      fontFamily: 'inherit',
                      fontSize: '0.85rem',
                      width: '200px',
                    }}
                  />
                </div>
              ))}
            </div>
          )}

          <button
            onClick={analyzeBids}
            disabled={loading || files.length === 0}
            style={{
              width: '100%',
              padding: '1rem',
              background: loading ? '#1a3050' : 'linear-gradient(135deg, #1a4d8f 0%, #0064ff 100%)',
              border: 'none',
              borderRadius: '6px',
              color: '#fff',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              fontFamily: 'inherit',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              transition: 'all 0.3s',
              boxShadow: loading ? 'none' : '0 4px 20px rgba(0, 100, 255, 0.3)',
            }}
          >
            {loading ? '⚙️ ANALYZING...' : '🔍 ANALYZE BIDS'}
          </button>

          {error && (
            <div style={{
              marginTop: '1rem',
              padding: '1rem',
              background: 'rgba(255, 68, 68, 0.1)',
              border: '1px solid #ff4444',
              borderRadius: '4px',
              color: '#ff8888',
              fontSize: '0.9rem',
            }}>
              ⚠️ {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        {analyses && (
          <>
            {/* Comparison Summary (if multiple bids) */}
            {analyses.comparison && (
              <div style={{
                background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 212, 255, 0.1) 100%)',
                border: '2px solid #00ff88',
                borderRadius: '8px',
                padding: '2rem',
                marginBottom: '2rem',
              }}>
                <div style={{
                  fontSize: '0.75rem',
                  color: '#00ff88',
                  letterSpacing: '0.15em',
                  marginBottom: '1rem',
                  textTransform: 'uppercase',
                }}>
                  AI RECOMMENDATION
                </div>
                <h2 style={{
                  margin: '0 0 1.5rem 0',
                  fontSize: '1.8rem',
                  color: '#00ff88',
                }}>
                  Winner: {analyses.comparison.recommended_bidder}
                </h2>
                <p style={{
                  fontSize: '1rem',
                  lineHeight: 1.6,
                  color: '#e0e6ed',
                  marginBottom: '1.5rem',
                }}>
                  {analyses.comparison.comparison_summary}
                </p>
                <div style={{
                  background: 'rgba(0, 0, 0, 0.3)',
                  padding: '1.5rem',
                  borderRadius: '6px',
                  border: '1px solid rgba(0, 255, 136, 0.2)',
                }}>
                  <div style={{
                    fontSize: '0.85rem',
                    color: '#00ff88',
                    marginBottom: '0.75rem',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                  }}>
                    Key Differentiators:
                  </div>
                  <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: 1.8 }}>
                    {analyses.comparison.key_differentiators.map((diff, i) => (
                      <li key={i} style={{ color: '#e0e6ed', fontSize: '0.95rem' }}>{diff}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Individual Bid Analyses */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: analyses.individual_analyses.length === 1 ? '1fr' : 'repeat(auto-fit, minmax(500px, 1fr))',
              gap: '2rem',
            }}>
              {analyses.individual_analyses.map((analysis, index) => (
                <div key={index} style={{
                  background: 'rgba(15, 22, 36, 0.8)',
                  border: '1px solid #1a4d8f',
                  borderRadius: '8px',
                  overflow: 'hidden',
                }}>
                  {/* Bid Header */}
                  <div style={{
                    background: 'linear-gradient(135deg, #1a4d8f 0%, #0f1624 100%)',
                    padding: '1.5rem',
                    borderBottom: '2px solid #4a8fe7',
                  }}>
                    <div style={{
                      fontSize: '0.75rem',
                      color: '#4a8fe7',
                      letterSpacing: '0.1em',
                      marginBottom: '0.5rem',
                      textTransform: 'uppercase',
                    }}>
                      BID #{index + 1}
                    </div>
                    <h3 style={{
                      margin: '0 0 0.75rem 0',
                      fontSize: '1.5rem',
                      color: '#00d4ff',
                    }}>
                      {analysis.bidder_name}
                    </h3>
                    <div style={{
                      fontSize: '0.85rem',
                      color: '#6b8cae',
                      fontFamily: 'sans-serif',
                    }}>
                      {analysis.filename}
                    </div>
                  </div>

                  <div style={{ padding: '1.5rem' }}>
                    {/* Score and Recommendation */}
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: '1fr 1fr',
                      gap: '1rem',
                      marginBottom: '1.5rem',
                    }}>
                      <div style={{
                        background: 'rgba(0, 100, 255, 0.1)',
                        border: '1px solid #1a4d8f',
                        borderRadius: '6px',
                        padding: '1rem',
                        textAlign: 'center',
                      }}>
                        <div style={{
                          fontSize: '0.75rem',
                          color: '#6b8cae',
                          marginBottom: '0.5rem',
                          letterSpacing: '0.1em',
                        }}>
                          SCORE
                        </div>
                        <div style={{
                          fontSize: '2.5rem',
                          fontWeight: 700,
                          color: '#4a8fe7',
                        }}>
                          {analysis.overall_score}/10
                        </div>
                      </div>
                      <div style={{
                        background: 'rgba(0, 100, 255, 0.1)',
                        border: '1px solid #1a4d8f',
                        borderRadius: '6px',
                        padding: '1rem',
                        textAlign: 'center',
                      }}>
                        <div style={{
                          fontSize: '0.75rem',
                          color: '#6b8cae',
                          marginBottom: '0.5rem',
                          letterSpacing: '0.1em',
                        }}>
                          STATUS
                        </div>
                        <div style={{
                          fontSize: '0.85rem',
                          fontWeight: 600,
                          color: getRecommendationColor(analysis.recommendation),
                          letterSpacing: '0.05em',
                        }}>
                          {analysis.recommendation}
                        </div>
                      </div>
                    </div>

                    {/* Summary */}
                    <div style={{ marginBottom: '1.5rem' }}>
                      <div style={{
                        fontSize: '0.85rem',
                        color: '#4a8fe7',
                        marginBottom: '0.75rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.1em',
                      }}>
                        Executive Summary
                      </div>
                      <p style={{
                        fontSize: '0.95rem',
                        lineHeight: 1.6,
                        color: '#e0e6ed',
                        margin: 0,
                        fontFamily: 'sans-serif',
                      }}>
                        {analysis.summary}
                      </p>
                    </div>

                    {/* Pros and Cons */}
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: '1fr 1fr',
                      gap: '1rem',
                      marginBottom: '1.5rem',
                    }}>
                      <div>
                        <div style={{
                          fontSize: '0.85rem',
                          color: '#00ff88',
                          marginBottom: '0.75rem',
                          textTransform: 'uppercase',
                          letterSpacing: '0.1em',
                        }}>
                          ✓ Strengths
                        </div>
                        <ul style={{
                          margin: 0,
                          padding: 0,
                          listStyle: 'none',
                        }}>
                          {analysis.pros.map((pro, i) => (
                            <li key={i} style={{
                              fontSize: '0.85rem',
                              color: '#e0e6ed',
                              marginBottom: '0.5rem',
                              paddingLeft: '1.25rem',
                              position: 'relative',
                              lineHeight: 1.5,
                            }}>
                              <span style={{
                                position: 'absolute',
                                left: 0,
                                color: '#00ff88',
                              }}>+</span>
                              {pro}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <div style={{
                          fontSize: '0.85rem',
                          color: '#ff8888',
                          marginBottom: '0.75rem',
                          textTransform: 'uppercase',
                          letterSpacing: '0.1em',
                        }}>
                          ⚠ Concerns
                        </div>
                        <ul style={{
                          margin: 0,
                          padding: 0,
                          listStyle: 'none',
                        }}>
                          {analysis.cons.map((con, i) => (
                            <li key={i} style={{
                              fontSize: '0.85rem',
                              color: '#e0e6ed',
                              marginBottom: '0.5rem',
                              paddingLeft: '1.25rem',
                              position: 'relative',
                              lineHeight: 1.5,
                            }}>
                              <span style={{
                                position: 'absolute',
                                left: 0,
                                color: '#ff8888',
                              }}>-</span>
                              {con}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Risk Assessment */}
                    <div style={{
                      background: 'rgba(0, 0, 0, 0.3)',
                      border: `1px solid ${getRiskColor(analysis.risks.level)}`,
                      borderRadius: '6px',
                      padding: '1rem',
                      marginBottom: '1.5rem',
                    }}>
                      <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: '0.75rem',
                      }}>
                        <div style={{
                          fontSize: '0.85rem',
                          color: '#6b8cae',
                          textTransform: 'uppercase',
                          letterSpacing: '0.1em',
                        }}>
                          Risk Assessment
                        </div>
                        <div style={{
                          fontSize: '0.85rem',
                          fontWeight: 600,
                          color: getRiskColor(analysis.risks.level),
                          letterSpacing: '0.05em',
                        }}>
                          {analysis.risks.level} RISK
                        </div>
                      </div>
                      <ul style={{
                        margin: 0,
                        paddingLeft: '1.5rem',
                        fontSize: '0.85rem',
                        color: '#e0e6ed',
                        lineHeight: 1.6,
                      }}>
                        {analysis.risks.details.map((risk, i) => (
                          <li key={i}>{risk}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Categories */}
                    {analysis.categories && analysis.categories.length > 0 && (
                      <div style={{ marginBottom: '1.5rem' }}>
                        <div style={{
                          fontSize: '0.85rem',
                          color: '#4a8fe7',
                          marginBottom: '0.75rem',
                          textTransform: 'uppercase',
                          letterSpacing: '0.1em',
                        }}>
                          Cost Breakdown
                        </div>
                        <div style={{
                          background: 'rgba(0, 0, 0, 0.3)',
                          border: '1px solid #1a4d8f',
                          borderRadius: '6px',
                          overflow: 'hidden',
                        }}>
                          {analysis.categories.map((cat, i) => (
                            <div key={i} style={{
                              padding: '0.75rem 1rem',
                              borderBottom: i < analysis.categories.length - 1 ? '1px solid #1a4d8f' : 'none',
                              display: 'flex',
                              justifyContent: 'space-between',
                              fontSize: '0.85rem',
                            }}>
                              <span style={{ color: '#e0e6ed' }}>{cat.name}</span>
                              <span style={{ color: '#4a8fe7', fontWeight: 600 }}>
                                {cat.amount} {cat.percentage && `(${cat.percentage})`}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Recommendation Rationale */}
                    <div style={{
                      background: 'rgba(0, 100, 255, 0.05)',
                      border: '1px solid #1a4d8f',
                      borderRadius: '6px',
                      padding: '1rem',
                    }}>
                      <div style={{
                        fontSize: '0.85rem',
                        color: '#4a8fe7',
                        marginBottom: '0.5rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.1em',
                      }}>
                        Recommendation
                      </div>
                      <p style={{
                        fontSize: '0.9rem',
                        lineHeight: 1.6,
                        color: '#e0e6ed',
                        margin: 0,
                        fontFamily: 'sans-serif',
                      }}>
                        {analysis.recommendation_rationale}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <div style={{
        borderTop: '1px solid #1a4d8f',
        padding: '2rem',
        textAlign: 'center',
        color: '#6b8cae',
        fontSize: '0.85rem',
        marginTop: '4rem',
      }}>
        <div>Bid Leveling AI © 2025 • Powered by Anthropic Claude</div>
        <div style={{ marginTop: '0.5rem', fontSize: '0.75rem' }}>
          Advanced AI-driven construction procurement analysis
        </div>
      </div>
    </div>
  );
}
