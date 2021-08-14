import ROOT, rootpy, root_numpy
import matplotlib
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt
import pandas
import numpy as np
import rootpy.plotting.root2matplotlib as rplt
import torch, math
from torch.autograd import Variable
import time

np.set_printoptions(precision=3, linewidth=200)

print "loading data"
df = pandas.DataFrame(
    root_numpy.root2array(
        "/mnt/t3nfs01/data01/shome/jpata/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",
#        stop=1000000
    )
)

bin_edges = np.linspace(0,300,100)
qh, _ = np.histogram(df["Quark_pt"], bins=bin_edges)

inds = np.searchsorted(bin_edges, df["Quark_pt"], side="left")
inds[inds>=98] = 98
df["weights"] = 1.0/qh[inds].astype(np.float32)

sel = (df["Quark_num_matches"]==1) & (df["Jet_pt"] < 400)
dfsel = df[sel]

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
D_in, H, D_out = 3, 100, 6
batch_size = 10000
n_epoch = 500

print "creating inputs", len(dfsel)
#dfsel_q = dfsel[(dfsel["Quark_pt"] > 200) & (dfsel["Quark_pt"] < 210)]
dfsel_q = dfsel[(dfsel["Quark_pt"] < 300)]
print "quark pt sel", len(dfsel_q)
dfsel_q = dfsel_q[:1000000]
print "subsample", len(dfsel_q)

print "quark pt mean", dfsel_q["Quark_pt"].mean(), "std", dfsel_q["Quark_pt"].std()
print "jet pt mean", dfsel_q["Jet_pt"].mean(), "std", dfsel_q["Jet_pt"].std()

# Create random Tensors to hold inputs and outputs, and wrap them in Variables.
x = Variable(torch.Tensor(dfsel_q[["Jet_pt"]].as_matrix().reshape(len(dfsel_q), 1).astype(np.float32)), requires_grad=False)
x = torch.stack([
    x,
    torch.sqrt(x),
    torch.pow(x, 2),
    Variable(torch.Tensor(dfsel_q[["Jet_eta"]].as_matrix().reshape(len(dfsel_q))), requires_grad=False),
    ], dim=1)[:, :, 0]
y = Variable(torch.Tensor(dfsel_q[["Quark_pt"]].as_matrix().reshape(len(dfsel_q), 1).astype(np.float32)), requires_grad=False)

w = Variable(torch.Tensor(dfsel_q[["weights"]].as_matrix().reshape(len(dfsel_q), 1).astype(np.float32)), requires_grad=False)

print "creating network"

D_in = x.shape[1]
H = 200
D_out = 6

model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.BatchNorm1d(H),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.5),
    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#   
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
#    
#    torch.nn.Linear(H, H),
#    torch.nn.BatchNorm1d(H),
#    torch.nn.ReLU(),
#    torch.nn.Dropout(0.5),
    
    torch.nn.Linear(H, D_out),
)

losses = []

def logpdf(_x, _y, _p):

    sigma1 = torch.exp(torch.clamp(_p[:, 0:1], -2, 6)) + 1
    sigma2 = torch.exp(torch.clamp(_p[:, 1:2], -2, 6)) + 1
    mu1 = _p[:, 2:3]
    mu2 = _p[:, 3:4]
    alpha1 = torch.exp(torch.clamp(_p[:, 4:5], -5, 5))
    alpha2 = torch.exp(torch.clamp(_p[:, 5:6], -5, 5))

    norm_alpha1 = alpha1/(alpha1+alpha2)
    norm_alpha2 = alpha2/(alpha1+alpha2)

    stpi = math.sqrt(2*math.pi)
    c1 = -0.5*torch.pow((_x[:, 0:1] - _y - mu1)/sigma1, 2)
    c2 = -0.5*torch.pow((_x[:, 0:1] - _y - mu2)/sigma2, 2)

    #v = (1.0/(sigma1*stpi))*torch.exp(c1)
    v = norm_alpha1*(1.0/(sigma1*stpi))*torch.exp(c1) + norm_alpha2*(1.0/(sigma2*stpi))*torch.exp(c2)

    v = torch.log(torch.clamp(v, 10**-16, 10**16))
#    if np.sum(np.isnan(v.data.numpy())) > 0:
#        import pdb
#        pdb.set_trace()
    #del sigma1, sigma2, mu1, mu2, alpha1, alpha2, c1, c2, norm_alpha1, norm_alpha2

    return v

def lh_loss(_y_pred, _x, _y, weights):
    ll = logpdf(_x, _y, _y_pred)*weights
    return -torch.mean(ll)

optimizer = torch.optim.Adam(
    model.parameters(), lr=0.001
)

print "starting training"

grad_means = []
grad_std = []

tprev = 0
tcur = 0
for iEpoch in range(n_epoch):
    losses_batch = []
    for mb in xrange(0, len(x), batch_size):
        y_pred = model(x[mb:mb+batch_size])
        
        loss = lh_loss(y_pred, x[mb:mb+batch_size], y[mb:mb+batch_size], w[mb:mb+batch_size])

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm(model.parameters(), 2)
        optimizer.step()
        
        losses_batch += [loss.data[0]]
        #l = []
        #for mp in model.parameters():
        #    l += [mp.grad.data.numpy().flatten()]

        #tot = np.hstack(l).flatten()
        #grad_means += [np.mean(tot)]
        #grad_std += [np.std(tot)]
    
#    print "l0 W", model[0].weight.data.numpy()
#    print "l0 b", model[0].bias.data.numpy()
#    print "l1 W", model[-1].weight.data.numpy()
#    print "l1 b", model[-1].bias.data.numpy()

#    y_pred = model(x[:10, :])
#    p = logpdf(x[:10], y[:10], y_pred)
#    data = np.hstack([x[:10, 0:1].data.numpy().astype(np.float32), y[:10].data.numpy().astype(np.float32), y_pred.data.numpy().astype(np.float32), p.data.numpy().astype(np.float32)])
#    data[:, 2] = np.exp(data[:, 2])
#    data[:, 3] = np.exp(data[:, 3])
#    data[:, -1] = np.exp(data[:, -1])
#    print "data", data
    
    tot_loss = np.mean(losses_batch)
    losses += [tot_loss]

    tcur = time.time()

    print iEpoch, tot_loss, tcur - tprev
    tprev = tcur

plt.figure(figsize=(5,5))
plt.plot(losses[10:])
#plt.yscale("log")
plt.savefig("loss.pdf")

#plt.figure(figsize=(5,5))
#plt.errorbar(range(len(grad_means)), grad_means, grad_std)
#plt.savefig("grad.pdf")

y_pred = model(x)
aas = np.sort(np.hstack([x[:, 0:1].data.numpy(), y_pred.data.numpy()]), axis=0)

plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.plot(aas[:, 0], aas[:, 3])
plt.title("mu1")

plt.subplot(2,2,2)
plt.plot(aas[:, 0], aas[:, 4])
plt.title("mu2")

plt.subplot(2,2,3)
plt.plot(aas[:, 0], np.exp(np.clip(aas[:, 1], -2, 7)) + 1)
plt.title("sigma1")

plt.subplot(2,2,4)
plt.plot(aas[:, 0], np.exp(np.clip(aas[:, 2], -2, 7)) + 1)
plt.title("sigma2")

plt.savefig("pars.pdf")

xvals = np.linspace(0, 500, 100)
for i in range(20):
    plt.figure(figsize=(5,5))
    yvals = y[i].data.numpy()[0]*np.ones(100)
    vs = []
    for _x, _y in zip(xvals, yvals):
        p = logpdf(Variable(torch.Tensor([[_x]])), Variable(torch.Tensor([[_y]])), y_pred[i:i+1]).data.numpy()[0,0]
        vs += [np.exp(p)]
    plt.plot(xvals, vs)
    q = (dfsel["Quark_pt"]>=y[i].data.numpy()[0]-2) & (dfsel["Quark_pt"]<y[i].data.numpy()[0]+2)
    plt.hist(dfsel[q]["Jet_pt"], bins=xvals, normed=True)
    plt.savefig("distr_{0}.pdf".format(i))
