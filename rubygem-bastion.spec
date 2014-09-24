# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%if "%{?scl}" == "ruby193"
    %global scl_ruby /usr/bin/ruby193-ruby
    %global scl_rake /usr/bin/ruby193-rake
    ### TODO temp disabled for SCL
    %global nodoc 1
%else
    %global scl_ruby /usr/bin/ruby
    %global scl_rake /usr/bin/rake
%endif

%global gem_name bastion

%define rubyabi 1.9.1
%global foreman_dir /usr/share/foreman
%global foreman_bundlerd_dir %{foreman_dir}/bundler.d

Summary:    MaaS Discovery Plugin for Foreman
Name:       %{?scl_prefix}rubygem-%{gem_name}
Version:    0.1.0
Release:    1%{?dist}
Group:      Applications/System
License:    GPLv3
URL:        http://github.com/katello/bastion
Source0:    http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires: foreman >= 1.6.0
Requires: %{?scl_prefix}rubygem-less-rails
Requires: %{?scl_prefix}rubygem-angular-rails-templates >= 0.0.4

BuildRequires: foreman >= 1.6.0
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygems
BuildRequires: %{?scl_prefix}rubygem-less-rails
BuildRequires: %{?scl_prefix}rubygem-angular-rails-templates >= 0.0.4


BuildArch: noarch

Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Bastion serves as a plugin to Foreman that provides common
elements for an AngularJS based UI component for a feature. 
The structure, common elements, and development tasks serve as
a basis for any plugin to quickly scaffold and create a UI that
takes advantage of the Foreman (or Foreman plugin) API to create
a modern UI.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} --no-rdoc --no-ri
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p ./usr/share
cp -r %{foreman_dir} ./usr/share || echo 0

pushd ./usr/share/foreman
export GEM_PATH=%{gem_dir}:%{buildroot}%{gem_dir}

cat <<GEMFILE > ./bundler.d/%{gem_name}.rb
group :bastion do
  gem '%{gem_name}'
end
GEMFILE

unlink tmp

export BUNDLER_EXT_NOSTRICT=1
export BUNDLER_EXT_GROUPS="default assets bastion"
%{scl_rake} plugin:assets:precompile['bastion'] RAILS_ENV=production --trace

popd
rm -rf ./usr

mkdir -p %{buildroot}%{foreman_bundlerd_dir}
cat <<GEMFILE > %{buildroot}%{foreman_bundlerd_dir}/%{gem_name}.rb
group :bastion do
  gem '%{gem_name}'
end
GEMFILE

mkdir -p %{buildroot}%{foreman_dir}/public/assets
ln -s %{gem_instdir}/public/assets/bastion %{buildroot}%{foreman_dir}/public/assets/bastion

%files
%dir %{gem_instdir}
%{gem_instdir}/app
%{gem_instdir}/lib
%{gem_instdir}/config
%{gem_instdir}/vendor
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_dir}/%{gem_name}.rb
%{foreman_dir}/public/assets/bastion
%{gem_instdir}/public/assets/bastion

%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/.jshintrc
%exclude %{gem_instdir}/grunt
%exclude %{gem_instdir}/bastion.js
%exclude %{gem_instdir}/Gruntfile.js
%exclude %{gem_instdir}/bower.json
%exclude %{gem_instdir}/package.json
%exclude %{gem_dir}/cache/%{gem_name}-%{version}%{?prever}.gem

%files doc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
