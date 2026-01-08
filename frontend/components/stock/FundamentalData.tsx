interface FundamentalDataProps {
  data: any;
}

export default function FundamentalData({ data }: FundamentalDataProps) {
  const { data: fundamentals, analysis } = data;

  const getValuationBadge = (valuation: string) => {
    const badges: any = {
      undervalued: { text: 'Unterbewertet', color: 'bg-success text-white' },
      'fairly valued': { text: 'Fair bewertet', color: 'bg-muted text-muted-foreground' },
      overvalued: { text: 'Überbewertet', color: 'bg-danger text-white' },
    };
    const badge = badges[valuation] || badges['fairly valued'];
    return <span className={`px-3 py-1 rounded-full text-sm font-medium ${badge.color}`}>{badge.text}</span>;
  };

  return (
    <div className="bg-card border rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Fundamentalanalyse</h2>

      {/* Valuation */}
      {analysis.valuation && (
        <div className="mb-6 p-4 bg-accent rounded-lg">
          <div className="text-sm text-muted-foreground mb-2">Bewertung</div>
          {getValuationBadge(analysis.valuation)}
        </div>
      )}

      {/* Key Metrics */}
      <div className="space-y-4">
        {/* Valuation Ratios */}
        <Section title="Bewertungskennzahlen">
          {fundamentals.pe_ratio !== null && (
            <MetricRow
              label="KGV (P/E Ratio)"
              value={fundamentals.pe_ratio.toFixed(2)}
              sectorAvg={fundamentals.sector_avg_pe}
            />
          )}
          {fundamentals.pb_ratio !== null && (
            <MetricRow
              label="KBV (P/B Ratio)"
              value={fundamentals.pb_ratio.toFixed(2)}
              sectorAvg={fundamentals.sector_avg_pb}
            />
          )}
          {fundamentals.ps_ratio !== null && (
            <MetricRow label="KUV (P/S Ratio)" value={fundamentals.ps_ratio.toFixed(2)} />
          )}
          {fundamentals.peg_ratio !== null && (
            <MetricRow label="PEG Ratio" value={fundamentals.peg_ratio.toFixed(2)} />
          )}
        </Section>

        {/* Profitability */}
        <Section title="Rentabilität">
          {fundamentals.profit_margin !== null && (
            <MetricRow
              label="Gewinnmarge"
              value={`${(fundamentals.profit_margin * 100).toFixed(2)}%`}
            />
          )}
          {fundamentals.operating_margin !== null && (
            <MetricRow
              label="Operative Marge"
              value={`${(fundamentals.operating_margin * 100).toFixed(2)}%`}
            />
          )}
          {fundamentals.return_on_equity !== null && (
            <MetricRow label="ROE" value={`${(fundamentals.return_on_equity * 100).toFixed(2)}%`} />
          )}
          {fundamentals.return_on_assets !== null && (
            <MetricRow
              label="ROA"
              value={`${(fundamentals.return_on_assets * 100).toFixed(2)}%`}
            />
          )}
        </Section>

        {/* Dividends */}
        {fundamentals.dividend_yield !== null && (
          <Section title="Dividende">
            <MetricRow
              label="Dividendenrendite"
              value={`${(fundamentals.dividend_yield * 100).toFixed(2)}%`}
            />
            {fundamentals.payout_ratio !== null && (
              <MetricRow
                label="Ausschüttungsquote"
                value={`${(fundamentals.payout_ratio * 100).toFixed(2)}%`}
              />
            )}
          </Section>
        )}

        {/* Growth */}
        <Section title="Wachstum">
          {fundamentals.revenue_growth !== null && (
            <MetricRow
              label="Umsatzwachstum (YoY)"
              value={`${(fundamentals.revenue_growth * 100).toFixed(2)}%`}
              isPositive={fundamentals.revenue_growth > 0}
            />
          )}
          {fundamentals.earnings_growth !== null && (
            <MetricRow
              label="Gewinnwachstum (YoY)"
              value={`${(fundamentals.earnings_growth * 100).toFixed(2)}%`}
              isPositive={fundamentals.earnings_growth > 0}
            />
          )}
        </Section>

        {/* Financial Health */}
        <Section title="Finanzielle Gesundheit">
          {fundamentals.debt_to_equity !== null && (
            <MetricRow label="Verschuldungsgrad" value={fundamentals.debt_to_equity.toFixed(2)} />
          )}
          {fundamentals.current_ratio !== null && (
            <MetricRow label="Current Ratio" value={fundamentals.current_ratio.toFixed(2)} />
          )}
        </Section>
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="font-semibold text-sm text-muted-foreground mb-2">{title}</h3>
      <div className="space-y-2">{children}</div>
    </div>
  );
}

function MetricRow({
  label,
  value,
  sectorAvg,
  isPositive,
}: {
  label: string;
  value: string;
  sectorAvg?: number;
  isPositive?: boolean;
}) {
  return (
    <div className="flex items-center justify-between p-2 rounded hover:bg-accent transition-colors">
      <span className="text-sm">{label}</span>
      <div className="text-right">
        <div
          className={`text-sm font-medium ${
            isPositive !== undefined
              ? isPositive
                ? 'text-success'
                : 'text-danger'
              : ''
          }`}
        >
          {value}
        </div>
        {sectorAvg && (
          <div className="text-xs text-muted-foreground">Sektor: {sectorAvg.toFixed(2)}</div>
        )}
      </div>
    </div>
  );
}
