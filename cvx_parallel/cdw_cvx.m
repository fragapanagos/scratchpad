function cdw_cvx(idx)
load(['A' num2str(idx) '.mat'])
load(['y' num2str(idx) '.mat'])
load(['decode_params' num2str(idx) '.mat'])

FPGA_MAX = params(1);
beta = params(2);
gamma = params(3);
min_w = params(4);

[~, n_neurons] = size(A);
[m, n_dim] = size(y);

cvx_begin
    variable d_weights(n_neurons, n_dim);
    minimize norm(A*d_weights - y, 2) + beta*norm(d_weights,1) + gamma*norm(d_weights,2);
    subject to
        % limit length of each neuron's decoding vector 
        d_weights <= FPGA_MAX
        d_weights >= min_w
        %sum(weights.^2, 2) <= upperbound^2; 
cvx_end 

save(['d_weights' num2str(idx) '.mat'], 'd_weights');
